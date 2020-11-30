from flask import Flask, jsonify, request, make_response
from flask.cli import AppGroup
from flask_dynamo import Dynamo
from datetime import datetime
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import json, sqlite3, sys
import boto3



app = Flask(__name__)


app.config['DYNAMO_ENABLE_LOCAL'] = True
app.config['DYNAMO_LOCAL_HOST'] = 'localhost'
app.config['DYNAMO_LOCAL_PORT'] = 8000
app.config['DYNAMO_TABLES'] = [
        dict(
            TableName='users',
            KeySchema=[
                {
                    'AttributeName': 'username',
                    'KeyType': 'HASH'
                }
            ],

            AttributeDefinitions=[
                {
                    'AttributeName': 'username',
                    'AttributeType': 'S'
                }
            ],

            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
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
                username = data['username']
                print("adding user:", username)
                dynamo.tables['users'].put_item(Item=data)
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

def get_items(user):
    response = dynamo.tables['users'].scan()
    return response["Items"]

def create_message(username, to, message, time):
    dynamo.tables['users'].put_item(Item={
        "username" : username,
        "to": to,
        "message": message,
        "time": time,
    })



# HELPER FUNCTIONS />---------------------------------------------------
