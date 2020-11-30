AUTHOR: Brandon Le
Project 5: NoSQL - INCOMPLETE - WILL COMPLETE BY 2ND SUBMISSION




Getting started

$ make                           #populates database
$ foreman start                  #starts services


API Implimentations (INCOMPLETE) Will complete by 2nd submission

sendDirectMessage(to, from, message)
    -Sends a direct message to a user. The quickReplies parameter is optional.

replyToDirectMessage(messageId, reply)
    -Replies to a direct message. The reply parameter may either be a text message or a quick-reply value.

listDirectMessagesFor(username)
    -Lists a user's DMs.

listRepliesTo(messageId)
    -Lists the replies to a DM.


Mock API examples

sendDirectMessage(to, from, message)
    $ curl -d '{"from":"billy", "to":"andy", "message":"Hello andy"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/dm

listDirectMessagesFor(username)
    $ 