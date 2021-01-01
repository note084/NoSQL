from flask import Flask, jsonify, request, make_response
from flask.cli import AppGroup
from flask_dynamo import Dynamo
from datetime import datetime
from decimal import Decimal
from datetime import datetime
import json, sqlite3, sys
import boto3


app = Flask(__name__)

import ddb

# < CUSTOM FUNCTIONS ---------------------------------------------------
@app.cli.command('init')
def init():
    ddb.init()
app.cli.add_command(init)

@app.cli.command('delete')
def delete():
    ddb.delete()
app.cli.add_command(delete)

# CUSTOM FUNCTIONS />---------------------------------------------------

# < API FUNCTIONS ------------------------------------------------------
@app.route('/')
def index():
    return "This is the main page."

@app.route('/user/<username>')
def listDirectMessagesFor(username):
    response = ddb.listDirectMessagesFor(username)
    return json.dumps(response, indent=2)

@app.route('/dm', methods=['POST'])
def direct_message():
    message = request.get_json(force=True)
    temp = ''
    if str(message['message']) == None or str(message['message']) == '':
        if str(message['quickreply']) == None or str(message['quickreply']) == '':
            return make_response("ERROR: MESSAGE NOT FOUND", 404)
        elif str(message['quickreply']) == '1':
            temp = 'Hello ' + str(message['to_username'])
        elif str(message['quickreply']) == '2':
            temp = 'How are you ' + str(message['to_username']) + '?'
        elif str(message['quickreply']) == '3':
            temp = 'Goodbye ' + str(message['to_username'])
        else:
            return make_response("ERROR: QUICK REPLY NOT FOUND", 404)
    else:
        temp = str(message['message'])

    if ddb.create_message(str(message['from_username']), str(message['to_username']), temp):
        return make_response("SUCCESS: MESSAGE POSTED", 201)
    else:
        return make_response("ERROR: CONFLICT", 409)

@app.route('/dm/reply/', methods=['POST'])
def reply_message():
    content = request.get_json(force=True)
    temp = ''
    if str(content['message']) == '1':
        temp = 'Hello'
    elif str(content['message']) == '2':
        temp = 'How are you?'
    elif str(content['message']) == '3':
        temp = 'Goodbye'
    else:
        return make_response("ERROR: CONFLICT", 409)
    if ddb.reply_message(str(content['message_ID']), str(content['from_username']), temp):
        return make_response("SUCCESS: REPLY POSTED", 201)
    else:
        return make_response("ERROR: DM NOT FOUND", 404)

@app.route('/dm/list/<messageid>')
def listReplies(messageid):
    response = ddb.listRepliesTo(messageid)
    return json.dumps(response, indent=2)

# API FUNCTIONS />------------------------------------------------------

if __name__ == '__main__':
    app.run()