from flask import Flask, jsonify, request, make_response
from flask.cli import AppGroup
from flask_dynamo import Dynamo
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from datetime import datetime
import json, sqlite3, sys
import boto3



app = Flask(__name__)


app.config['DYNAMO_ENABLE_LOCAL'] = True
app.config['DYNAMO_LOCAL_HOST'] = 'localhost'
app.config['DYNAMO_LOCAL_PORT'] = 8000
app.config['DYNAMO_TABLES'] = [
        dict(
            TableName='direct_messages',
            KeySchema=[
                {
                    'AttributeName': 'dm_id',
                    'KeyType': 'HASH'
                }
            ],

            AttributeDefinitions=[
                {
                    'AttributeName': 'dm_id',
                    'AttributeType': 'S'
                }
            ],

            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
]

dynamo = Dynamo(app)
schema = "populate.json"



# < HELPER FUNCTIONS --------------------------------------------------
def init():
    try:
        with app.app_context():
            dynamo.create_all()
            print("Tables created in dynamoDB...")
        with open(schema) as json_file:
            print("Populating Database...")
            datas = json.load(json_file, parse_float=Decimal)
            for data in datas:
                dm_id = data['dm_id']
                user1 = data['user1']
                user2 = data['user2']
                print("--------------------------------------")
                print("Adding Direct Message:", dm_id, "for", user1, "and", user2)
                for content in data['content']:
                    user = content['user']
                    message = content['message']
                    time = datetime.now()
                    content['timestamp'] = content['timestamp'].replace("", time.strftime("%B %d, %Y %H:%M:%S"))
                    time = content['timestamp']
                print("From:", user)
                print("Message:", message)
                print("Timestamp:", time)
                print("--------------------------------------")
                dynamo.tables['direct_messages'].put_item(Item=data)
            print("Finished Populating Database")
    except:
        print("Failed to create tables in dynamoDB")
        sys.exit()


def delete():
    try:
        dynamo.destroy_all()
        print("Deleted all tables in dynamoDB")

    except:
        print("Failed to delete tables in dynamoDB")
        sys.exit()

def listDirectMessagesFor(username):
    response = dynamo.tables['direct_messages'].scan()
    items = response["Items"]
    sort = []
    for item in items:
        if (item['user1'] == username) or (item['user2'] == username):
            if (item['user1'] == username):
                sort.append({'Message_ID': item['dm_id'], 'From': item['user1'], 'To': item['user2']})
            else:
                sort.append({'Message_ID': item['dm_id'], 'From': item['user2'], 'To': item['user1']})
    if sort == []:
        return False
    else:
        return sort

def listRepliesTo(messageID):
    response = dynamo.tables['direct_messages'].scan()
    items = response["Items"]
    sort = []
    for item in items:
        if (item['dm_id'] == messageID):
            sort.append(item['content'])
    if sort == []:
        return False
    else:
        return sort

def create_message(from_username, to_username, message):
    current = dynamo.tables['direct_messages'].scan()
    items = current["Items"]
    for item in items:
        if (item['user1'] == from_username and item['user2'] == to_username) or (item['user2'] == to_username and item['user1'] == from_username):
            return reply_message(item['dm_id'], from_username, message)
    time = datetime.now()
    length = len(items)
    dm = {
        "dm_id": str(length + 1),
        "user1": from_username,
        "user2": to_username,
        "content": [{ 
            "message_id": "1",
            "user": from_username,
            "message": message,
            "timestamp": time.strftime("%B %d, %Y %H:%M:%S")
            }]
    }
    dynamo.tables['direct_messages'].put_item(Item=dm)
    return True
    
def reply_message(messageID, username, reply):
    current = dynamo.tables['direct_messages'].scan()
    items = current["Items"]
    for item in items:
        if messageID == item['dm_id']:
            length = len(item['content'])
            time = datetime.now()
            message = {
                "message_id": str(length + 1),
                "user": username,
                "message": reply,
                "timestamp": time.strftime("%B %d, %Y %H:%M:%S")
            }
            item['content'].append(message)
            dynamo.tables['direct_messages'].put_item(Item=item)
            return True
    return False

# HELPER FUNCTIONS />---------------------------------------------------
