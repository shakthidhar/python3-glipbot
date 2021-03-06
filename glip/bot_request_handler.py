from core.rc_client_bot import RCClientBot
from glip.process_commands import handler as process_commands
from core.rc_client_helper import RCClientHelper
import json
import traceback

def handler(event):

    request_type = event['pathParameters']['request_type']
    rcclient_bot = RCClientBot()
    rcclient_helper = RCClientHelper()

    if request_type == 'oauth':
        try:
            bot_info = rcclient_bot.get_bot_info(event)
            rcclient_bot.save_token(bot_info)
            response = rcclient_bot.subscribe(bot_info['id'])
            return response
        except Exception as error:
            traceback.print_exc()
            response = {
                "statusCode": 500,
                "body": "could not add token to db"
            }
            return response
    elif request_type == 'oauth_prod':
        try:
            code = event['queryStringParameters']['code']
            creator_app_data={
                'creator_extension_id':event['queryStringParameters']['creator_extension_id'],
                'creator_account_id':event['queryStringParameters']['creator_account_id'],
                'client_id':event['queryStringParameters']['client_id']
            }
            rcclient_bot.auth_with_code(code)
            bot_info = rcclient_bot.get_bot_info_prod(creator_app_data)
            rcclient_bot.save_token(bot_info)
            response = rcclient_bot.subscribe(bot_info['id'])
            return response
        except Exception as error:
            traceback.print_exc()
            response = {
                "statusCode": 500,
                "body": "could not add token to db"
            }
            return response
    elif request_type == 'receive':
        #check if validation token exists
        #if it exists then respond with validation token
        #else process requests
        print('notifications from subscribtions')
        if event['headers'].get('Validation-Token') != None :
            print('received a validation token')
            validation_token = event['headers']['Validation-Token']
            response = {
                "statusCode": 200,
                "headers": {"Validation-Token": validation_token},
                "body": "",
            }
            return response
        else:
            print('Received an event notification')
            notification = json.loads(event['body'])
            body = notification['body']
            print(body)

            if body['eventType'] == 'GroupJoined':
                #New user has joined the group
                #Post welcome message with link to authorize helper
                group_id = body['id']
                bot_id = notification['ownerId']
                reply_message = process_commands(None,bot_id,group_id,'new group')
                rcclient_bot.post_message(bot_id,group_id,reply_message)

            elif body['eventType'] == 'PostAdded' and body['type'] == 'TextMessage':
                #Received a new text message
                #Check the text with existing commands and post 
                #and an appropriate message
                group_id = body['groupId']
                creator_id = body['creatorId']
                bot_id = notification['ownerId']
                received_message = body['text']
                
                #if notification is not for the message posted by the bot
                if creator_id != bot_id:
                    print('Received message from user')
                    reply_message = process_commands(creator_id,bot_id,group_id,received_message)
                    rcclient_bot.post_message(bot_id,group_id,reply_message)
                    #rcclient_bot.post_message_card(group_id,reply_message)
                else:
                    print('The bot posted: '+ received_message)
            #if event.type = 'create' do nothing
            elif body['eventType'] == 'Create':
                print('A new bot with account ID '+notification['ownerId']+' and extension ID '+ body['extensionId']+' has been created')

            elif body['eventType'] == 'Delete':
                bot_id = notification['ownerId']
                extension_id = body['extensionId']
                rcclient_bot.delete_token(bot_id)
                rcclient_helper.delete_token(bot_id)
                print('The bot with account ID '+bot_id+ ' and extension ID '+extension_id+' has been removed')

            response = {
                "statusCode": 200,
                "body": "",
            }
            return response