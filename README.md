# Twilio Bulk Sms
This is a tool for managing sms notififcation lists


### Setup
You need to do a few things in the Twilio admin panel to get this working, but I've already done them and this documentation is mainly for internal use. I will probably fully document this at some point but that point is not right now
### Configuration
Running this requires the following environment variables:

Required:
- `TWILIO_ACCOUNT_SID` - SID of your Twilio account
- `TWILIO_AUTH_TOKEN` - Auth token of your Twilio account 
- `TWILIO_NOTIFY_SERVICE_SID` - SID of your Twilio Notify Service (For sending messages)
- `DB_PASSWORD` password to the postgresql database

Optional:
- `DB_USERNAME` (Default "postgres"),
- `DB_DB` (Default "twilio-bulk-sms"),
- `DB_HOST` (Default "10.0.3.34")

## API
### Authentication
To access most endpoints, an `Authorization` header must be passed with a token from Auth0 that has the appropriate scope.
### Endpoints
The following endpoints are available:
- [/api/message](#post-apimessage)
- [/api/getGroups](#get-apigetgroups)
- [/api/getGroupName](#get-apigetgroupname)
- [/api/createGroup](#post-apicreategroup)
- [/api/addToGroup](#post-apiaddtogroup)
- [/api/removeFromGroup](#post--apiremovefromgroup)

#### POST /api/message
Required scope: `sms:send`

Sends a bulk sms to everyone in the group provided

Request body:

    {
        'message':'Contents of the message you want sent',
        'group_id':5
    }
#### GET /api/getGroups
Required scope: `sms:read`

Returns a list of every group, including the numbers in them  

No request data is expected

Response body:
    
    [
        {
            'name': 'Group #1',
            'id': 1,
            'numbers': ['+123456789', '+99999999']
        },
        {
            'name': 'Group #2',
            'id': 2,
            'numbers': ['+0889088889', '+85112244445']
        }
    ] 
#### GET /api/getGroupName
Required scope: N/A

gets the name of a group with the ID provided

Request body:

    {
        'group_id': 1
    }
    
Response body:

    {
        'name': 'Group #1'
    }
#### POST /api/createGroup
Required scope: `sms:write`

Creates a group with the specified `group_name`

Request body:

    {
        'group_name': 'Group #3'
    }
#### POST /api/addToGroup
Required scope: N/A

Adds a `number` to specified group by `group_id`

Note: This should be in [E.164](https://www.twilio.com/docs/glossary/what-e164) format. If it is not E.164, an automatic conversion will be attempted. Additionally the number will be verified and validated, with errors thrown if there is a problem with the number.

Request body:

    {
        'group_id': 2,
        'number': '+81814802108'
    }
#### POST  /api/removeFromGroup