from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import sys

app = Flask(__name__)
response_add = False
response_remove = False
grocery_list = ['apples', 'bananas']


@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    body = body.lower()

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if response_add == True:
        grocery_list.append(body)
        clean_list = '\n'.join(grocery_list)
        resp.message("Added ", body,
                     " to the list. Your current list is: \n", clean_list)
        response_add = False

    elif response_remove == True:

        if body in grocery_list:
            grocery_list.remove(body)
            clean_list = '\n'.join(grocery_list)

            resp.message("Removed ", body,
                         " from the list. Your current list is: \n", clean_list)
            response_remove = False

    elif body.lower() == "add":
        resp.message("What would you like to add to your grocery list?")
        response_add = True

    elif body.lower() == "remove":
        resp.message("What would you like to remove from your grocery list?")
        response_remove = True
    elif body.lower() == "finished":
        resp.message("Grocery list completed")
    elif body.lower() == 'list':
        resp.message("Your current list is: \n", clean_list)
    else:
        resp.message("You sent", body,
                     "\nSend 'ADD' to add an item to a grocery list, Send 'REMOVE' to remove an item, send 'FINISHED' to delete grocery list, send 'LIST' to see current list.")

    return str(resp)

# Below is used for debugging and adding features, comment out when running this

# while True:
#     body = input("What would you like to do? Send 'ADD' to add an item to a grocery list, Send 'REMOVE' to remove an item, send 'FINISHED' to delete grocery list, send 'LIST' to see current list.\n")

#     if body.lower() == "add":
#         body = input("What would you like to add to your grocery list?\n")
#         body = body.lower()
#         grocery_list.append(body)
#         clean_list = '\n'.join(i for i in grocery_list)
#         print("Added ", body,
#               " to the list. Your current list is: \n", clean_list)

#     elif body.lower() == "remove":
#         body = input("What would you like to remove from your grocery list?\n")

#         if body in grocery_list:
#             grocery_list.remove(body)
#             clean_list = '\n'.join(i for i in grocery_list)

#             print("Removed ", body,
#                   " from the list. Your current list is: \n", clean_list)
#         else:
#             print(body, "not found in list")
#     elif body.lower() == "finished":
#         print("Grocery list completed")
#         sys.exit()
#     elif body.lower() == 'list':
#         print("Your current list is: \n", clean_list)
#     else:
#         print("You sent", body,
#               "\nSend 'ADD' to add an item to a grocery list, Send 'REMOVE' to remove an item, send 'FINISHED' to delete grocery list, send 'LIST' to see current list.")
