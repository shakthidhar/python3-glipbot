import boto3
from boto3.dynamodb.conditions import Key, Attr
import os
from urllib.parse import urlencode
from ringcentral import SDK
from urllib.parse import parse_qs
import logging
from botocore.exceptions import ClientError
from decimal import *
import traceback

dynamodb = boto3.resource('dynamodb')

class RCClientHelper:

    def __init__(self):
        self.rcsdk = SDK(os.environ['HELPER_CLIENT_ID'],os.environ['HELPER_CLIENT_SECRET'],os.environ['RINGCENTRAL_ENV'])
        self.platform = self.rcsdk.platform()

    def save_token(self,bot_id):
        try:
            data = self.platform.auth().data()
            print(data)

            data = {
                'owner_id':data['owner_id'],
                'bot_id':bot_id,
                'access_token': data['access_token'],
                'expire_time': Decimal(data['expire_time']),
                'expires_in': Decimal(data['expires_in']),
                'refresh_token': data['refresh_token'],
                'refresh_token_expire_time': Decimal(data['refresh_token_expire_time']),
                'refresh_token_expires_in': Decimal(data['refresh_token_expires_in']),
                'remember': data['remember'],
                'ex_scope': data['scope'],
                'token_type': data['token_type']
            }
            table = dynamodb.Table(os.environ['HELPER_DYNAMODB_TABLE'])
            table.put_item(Item=data)
            print('successfully added token to table!!')

        except Exception as error:
            print('failed to add token to table!!')
            logging.error(error)
            traceback.print_exc()
            raise error

    def delete_token(self,bot_id):
        table = dynamodb.Table(os.environ['HELPER_DYNAMODB_TABLE'])
        response = table.query(
            IndexName=os.environ['HELPER_BOT_ACCOUNT_RELATION'],
            KeyConditionExpression=Key('bot_id').eq(bot_id)
        )
        for item in response['Items']:
            table.delete_item(
                Key={
                    'owner_id': item['owner_id']
                }
            )
            
    
    # def save_bot_and_group_id(self, owner_id, bot_id, group_id):
    #     data = {
    #         'owner_id':owner_id,
    #         'bot_id':bot_id,
    #     }
    #     table = dynamodb.Table(os.environ['HELPER_DYNAMODB_TABLE'])
    #     table.put_item(Item=data)
    #     print('Account Id, Bot Id and Group Id have been added to the table.')


    def add_token_to_platform(self,item):
        #add the retrived values to the platform
        self.platform.auth().set_data(item)

    def auth_with_code(self,code):
        #authorize with code
        try:
            redirect_url = os.environ['REDIRECT_HOST']+'/helper/oauth'
            print('redirect_url: '+redirect_url)
            self.platform.login(code=code,redirect_uri=redirect_url)
        except Exception as error:
            logging.error(error)
            raise error
    
    def get_auth_url(self,group_id,bot_id):
        #get the url the user can use to authorize the helper app
        redirect_url = os.environ['REDIRECT_HOST']+'/helper/oauth'
        host = os.environ['RINGCENTRAL_ENV']
        query = urlencode({
            'response_type': 'code',
            'redirect_uri': redirect_url,
            'client_id': os.environ['HELPER_CLIENT_ID'],
            'state': group_id+','+bot_id,
            'brand_id': '',
            'display': '',
            'prompt': '',
            'localeId': '',
            'ui_locales': '',
            'ui_options': ''
        })

        return f'{host}/restapi/oauth/authorize?{query}'

    def get_token_from_db(self,owner_id):
        #return the table item for the given account id
        table = dynamodb.Table(os.environ['HELPER_DYNAMODB_TABLE'])
        
        try:
            result = table.get_item(
                Key={
                    'owner_id': owner_id
                }
            )
            return result['Item']
        except Exception as error:
            logging.error(error)
            return None

    def has_valid_token(self,owner_id,bot_id):
        item = self.get_token_from_db(owner_id) 
        if item == None:
            return False
        else:
            self.add_token_to_platform(item)
            if self.platform.auth().access_token_valid():
                print('Has valid access token!')
                print(self.platform.auth().data())
                return True
            elif self.platform.auth().refresh_token_valid():
                print('Has valid refresh token')
                self.platform.refresh()
                self.save_token(bot_id)
                return True
            else:
                print('Has invalid access and refresh token')
                return False

    def get(self, url, query_params):
        print('getting info from ringcentral platform')
        ret_val = self.platform.get(url,query_params=query_params)
        print(ret_val.json_dict())
        return ret_val.json_dict()

    def put(self, url, body):
        print('updating ringcentral settings')
        self.platform.put(url,body=body)