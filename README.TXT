AUTHOR: Brandon Le, Gerardo Pena, Kyle Ear
Project 5: NoSQL - COMPLETE

***Requirements***
Must have DynamoDB set up locally on your computer.
Instructions on how to set up DynamoDB locally in the link below.
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html

***Getting started***

1. Start DynamoDB locally on your computer. 
-Open a command prompt window, navigate to the directory where you extracted DynamoDBLocal.jar, and enter the following command.

$ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb

2. Start services
-Open a command prompt window, navigate to the directory where you extracted this repository from and enter the following commands.

$ make                           #populates database with json data in populate.json
$ foreman start                  #starts services

*Optional command*
$ flask delete                   #deletes all generated tables in DynamoDB


***API Implimentations***

sendDirectMessage(from_username, to_username, message)
    -Sends a direct message to a user. The quickReplies parameter is optional.

replyToDirectMessage(messageID, from_username, reply)
    -Replies to a direct message.

listDirectMessagesFor(username)
    -Lists a user's DMs.

listRepliesTo(messageId)
    -Lists the replies to a DM.


***Mock API examples***

sendDirectMessage(to, from, message)
    $ curl -d '{"from_username":"Brandon", "to_username":"Gerardo", "message":"Sending DM to Gerardo"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/dm

listDirectMessagesFor(username)
    $ curl http://127.0.0.1:5000/user/b1

replyToDirectMessage()
    $ curl -d '{"message_ID":"1",  "from_username":"b1", "message":"Test"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/dm/reply/

listRepliesTo(messageId)
    $ curl http://127.0.0.1:5000/dm/list/1