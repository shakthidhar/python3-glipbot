import boto3
import os
from ringcentral import SDK
from urllib.parse import parse_qs
import logging
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')

class RCClientBot:

    def __init__(self):
        self.rcsdk = SDK(os.environ['BOT_CLIENT_ID'],os.environ['BOT_CLIENT_SECRET'],os.environ['RINGCENTRAL_ENV'])
        self.platform = self.rcsdk.platform()
    
    def get_bot_info(self,event):
        body = parse_qs(event['body'])
        print(event)
        header = {
                'Authorization': 'bearer ' + body['access_token'][0]
        }
        bot_extension_info = self.platform.get('/account/~/extension/~', headers=header, skip_auth_check=True)
        bot_extension_info = bot_extension_info.json_dict()
        bot_info = {
            'id':str(bot_extension_info['id']),
            'extension':str(bot_extension_info['extensionNumber']),
            'access_token': body['access_token'][0],
            'client_id': body['client_id'][0],
            'creator_extension_id': body['creator_extension_id'][0],
            'creator_account_id': body['creator_account_id'][0],
        }
        return bot_info

    def get_bot_info_prod(self,creator_app_data):
        data = self.platform.auth().data()
        header = {
                'Authorization': 'bearer ' + data['access_token']
        }
        bot_extension_info = self.platform.get('/account/~/extension/~', headers=header, skip_auth_check=True)
        bot_extension_info = bot_extension_info.json_dict()
        bot_info = {
            'id':str(bot_extension_info['id']),
            'extension':str(bot_extension_info['extensionNumber']),
            'access_token': data['access_token'],
            'client_id': creator_app_data['client_id'],
            'creator_extension_id': creator_app_data['creator_extension_id'],
            'creator_account_id': creator_app_data['creator_account_id'],
        }
        return bot_info

    def save_token(self, bot_info):
        table = dynamodb.Table(os.environ['BOT_DYNAMODB_TABLE'])
        table.put_item(Item=bot_info)
        print('successfully added token to table!!')
    
    def delete_token(self,bot_id):
        table = dynamodb.Table(os.environ['BOT_DYNAMODB_TABLE'])
        table.delete_item(
            Key={
                'id': bot_id
            }
        )

    def auth_with_code(self, code):
        redirect_url = os.environ['REDIRECT_HOST']+'/bot/oauth_prod'
        print('redirect_url: '+redirect_url)
        self.platform.login(code=code,redirect_uri=redirect_url)
        print('data from platform:')
        print(self.platform.auth().data())

    def add_token_to_platform(self,bot_id):
        try:
            table = dynamodb.Table(os.environ['BOT_DYNAMODB_TABLE'])
            result = table.get_item(
                Key={
                    'id': bot_id
                }
            )
            data = self.platform.auth().data()
            print(result)
            print(result['Item'])
            data['access_token'] = result['Item']['access_token']
            data['token_type'] = 'bearer'
            data['expires_in'] = 500000000
            self.platform.auth().set_data(data)
            print('successfully got token from table')
            return True
        except Exception as error:
            print('failed to get token from table!!')
            logging.error(error)
            return False

    def subscribe(self,bot_id):
        print('subscribing..')
        if self.add_token_to_platform(bot_id):
            requestData = {
                "eventFilters": [
                #Get Glip Post Events
                "/restapi/v1.0/glip/posts",
                #Get Glip Group Events
                "/restapi/v1.0/glip/groups",
                #Get Bot Create/Remove events
                "/restapi/v1.0/account/~/extension/~"
            ],
            "deliveryMode": {
                "transportType": "WebHook",
                "address": os.environ['REDIRECT_HOST'] + "/bot/receive"
            },
            "expiresIn": 500000000
            }
            data = self.platform.auth().data()
            header = {
                'Authorization': 'bearer ' + data['access_token']
            }
            self.platform.post('/subscription',body=requestData, headers=header, skip_auth_check=True)
            
            response = {
                "statusCode": 200,
                "body": ""
            }
            return response
        else:
            response = {
                "statusCode": 500,
                "body": "could not add token to db"
            }
            return response

    def post_message(self,bot_id,group_id,message):
        if self.add_token_to_platform(bot_id):
            messageData = {
                "text":message
            }
            data = self.platform.auth().data()
            header = {
                'Authorization': 'bearer ' + data['access_token']
            }
            print('posted message '+message)
            self.platform.post('/restapi/v1.0/glip/groups/'+group_id+'/posts',body=messageData, headers=header, skip_auth_check=True)
        else:
            print("failed to add token to platform")


    def post_message_card(self,bot_id,group_id,message):
        if self.add_token_to_platform(bot_id):
            data = self.platform.auth().data()
            header = {
                'Authorization': 'bearer ' + data['access_token']
            }
            print('posted message ')
            print(message)
            self.platform.post('/restapi/v1.0/glip/groups/'+group_id+'/posts',body=message, headers=header, skip_auth_check=True)