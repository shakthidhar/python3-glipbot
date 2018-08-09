from core.rc_client_bot import RCClientBot
from glip.process_commands import handler as process_commands
from glip.lex.lex_client_handler import handler as lex_process_message
from core.rc_client_helper import RCClientHelper
import json
import traceback
import boto3
import os
import re

dynamodb = boto3.resource('dynamodb')
re_mention = r'!\[:Person\]\(([0-9]+)\)'

def save_group_id(group_id, total_members, bot_id):
    table = dynamodb.Table(os.environ['GROUP_LIST_DYNAMODB_TABLE'])
    group_info = {
        'group_id':group_id,
        'bot_id':bot_id,
        'total_members':total_members
    }
    table.put_item(Item=group_info)
    print('A record for the group has been created.')

def get_total_members(group_id, bot_id):
    table = dynamodb.Table(os.environ['GROUP_LIST_DYNAMODB_TABLE'])
    response = table.get_item(
        Key={
            'group_id': group_id,
            'bot_id': bot_id
        }
    )
    return response['Item']['total_members']

def update_group_id(group_id, total_members, bot_id):
    table = dynamodb.Table(os.environ['GROUP_LIST_DYNAMODB_TABLE'])
    response = table.update_item(
        Key = {
            'group_id':group_id,
            'bot_id': bot_id
        },
        UpdateExpression="set total_members = :tm",
        ExpressionAttributeValues={
            ':tm': total_members,
        },
        ReturnValues="ALL_NEW"
    )
    print('The number of members for the group '+group_id+' has been updated to '+str(response['Attributes']['total_members']))

def delete_group_id_by_bot_id(bot_id):
    table = dynamodb.Table(os.environ['GROUP_LIST_DYNAMODB_TABLE'])
    response = table.query(
        KeyConditionExpression=Key('bot_id').eq(bot_id)
    )
    
    for item in response['Items']:
        table.delete_item(
            Key={
                'group_id': item['group_id']
            }
        )

def delete_group_id_by_group_id(group_id, bot_id):
    table = dynamodb.Table(os.environ['GROUP_LIST_DYNAMODB_TABLE'])
    table.delete_item(
        Key={
            'group_id': group_id,
            'bot_id': bot_id,
        }
    )


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
            print(notification)
            print(body)

            if body['eventType'] == 'GroupJoined':
                #New Group or Private chat has bee created
                #Create an entry in the database 
                #Store groupId and number of participants in the group
                #Post welcome message with link to authorize helper
                group_id = body['id']
                bot_id = notification['ownerId']
                total_members = len(body['members'])
                save_group_id(group_id,total_members, bot_id)
                if total_members == 2:
                    reply_message = lex_process_message(None,bot_id,group_id,None,True)
                    rcclient_bot.post_message(bot_id,group_id,reply_message)
            
            elif body['eventType'] == 'GroupChanged':
                #update db with number of people in the table
                group_id = body['id']
                bot_id = notification['ownerId']
                total_members = len(body['members'])
                update_group_id(group_id,total_members, bot_id)
            
            elif body['eventType'] == 'GroupLeft':
                #bot has been romeved from the group so delete entry from the database
                group_id = body['id']
                bot_id = notification['ownerId']
                delete_group_id_by_group_id(group_id, bot_id)

            elif body['eventType'] == 'PostAdded' and body['type'] == 'TextMessage':

                #Received a new text message
                group_id = body['groupId']
                creator_id = body['creatorId']
                bot_id = notification['ownerId']
                received_message = body['text']

                if received_message == '':
                    #Group has been deleted.
                    #Delete group from db
                    group_id = body['groupId']
                    delete_group_id_by_group_id(group_id,bot_id)
                else:
                    total_members = get_total_members(group_id, bot_id)
                    #Check the text with existing intents and post 
                    #and an appropriate message
                    #if notification is not for the message posted by the bot
                    if creator_id != bot_id and total_members == 2:
                        print('Received message from user')
                        #reply_message = process_commands(creator_id,bot_id,group_id,received_message)
                        reply_message = lex_process_message(creator_id,bot_id,group_id,received_message)
                        rcclient_bot.post_message(bot_id,group_id,reply_message)
                        #rcclient_bot.post_message_card(group_id,reply_message)
                    elif creator_id != bot_id and total_members > 2:
                        matches = re.findall(re_mention, received_message)
                        if str(bot_id) in matches:
                            reply_message = 'Sorry, the bot is not meant to be used in teams with more than two members(including the bot).'
                            rcclient_bot.post_message(bot_id,group_id,reply_message)
                            print('Bot was mentioned in a group'+ received_message)
            #if event.type = 'create' do nothing
            elif body['eventType'] == 'Create':
                print('A new bot with account ID '+notification['ownerId']+' and extension ID '+ body['extensionId']+' has been created')

            elif body['eventType'] == 'Delete':
                bot_id = notification['ownerId']
                extension_id = body['extensionId']
                rcclient_bot.delete_token(bot_id)
                rcclient_helper.delete_token(bot_id)
                delete_group_id_by_bot_id(bot_id)
                print('The bot with account ID '+bot_id+ ' and extension ID '+extension_id+' has been removed')

            response = {
                "statusCode": 200,
                "body": "",
            }
            return response