import json

from flask import Flask, request
from flask_cors import CORS

from db.models import session_creator, Group, Number
from utils.request import validate_body
from utils.response import response, error_response
from utils.sms import send_bulk_sms

app = Flask(__name__)

CORS(app)


@app.route('/api/message', methods=['POST'])
def message_audience():
    body = request.get_json()
    status, missing_field = validate_body(body, ['message', 'phones'])
    if not status:
        return error_response(f'{missing_field} is missing')
    send_bulk_sms(body['phones'], body['message'])
    return response(True, 'Success', None)


@app.route('/api/getGroups', methods=['GET'])
def get_groups():
    session = session_creator()
    return json.dumps(session.query(Group).all())


@app.route('/api/createGroup', methods=['POST'])
def create_group():
    body = request.get_json()
    assert 'group_name' in body
    session = session_creator()
    session.add(
        Group(
            group_name=body['group_name']
        )
    )
    session.commit()
    session.close()
    return 'ok'


@app.route('/api/addToGroup', methods=['POST'])
def add_to_group():
    body = request.get_json()
    assert 'group_id' in body
    assert 'number' in body
    session = session_creator()
    # Todo: verify number is number
    group = session.query(Group).filter_by(id = body['group_id']).first()
    if group is not None:
        session.add(group)
        group.numbers.append(Number(number=body['number']))
        session.commit()
        session.close()
    else:
        session.rollback()
        session.close()
        return 'no group found'


@app.route('/api/removeFromGroup', methods=['POST'])
def remove_from_group():
    body = request.get_json()
    assert 'group_id' in body
    assert 'number' in body
    session = session_creator()
    group = session.query(Group).filter_by(id = body['group_id']).first()
    if group is not None:
        session.add(group)
        session.query(Number).filter(
            Number.number == body['number'], Number.group_id == body['group_id']
        ).delete()
        session.commit()
        session.close()
        return 'ok'
    else:
        session.rollback()
        session.close()
        return 'no group found'


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)