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

@app.cli.command('init')
def init():
    ddb.init()
app.cli.add_command(init)

@app.cli.command('delete')
def delete():
    ddb.delete()
app.cli.add_command(delete)


@app.route('/')
def index():
    return "This is the main page."


    
@app.route('/user/<user>')
def get_users(user):
    response = ddb.get_items(user)
    return jsonify(response)

@app.route('/dm', methods=['POST'])
def direct_message():
    message = request.get_json(force=True)
    time = datetime.now()
    ddb.create_message(str(message['from']), str(message['to']), str(message['message']), str(time))
    return make_response("SUCCESS: MESSAGE POSTED", 201)


if __name__ == '__main__':
    app.run()