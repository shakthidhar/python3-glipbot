from core.rc_client_helper import RCClientHelper
import logging
from glip.lex.lex_generate_responses import *
from glip.generate_update_body import *
import traceback
import json
from ringcentral.http.api_exception import ApiException
import boto3

lex_client = boto3.client('lex-runtime')
help_intent = 'Help'
helper = RCClientHelper()

def get_auth_url_msg(owner_id,bot_id,group_id):
    helper.save_bot_and_group_id(owner_id, bot_id, group_id)
    auth_url = helper.get_auth_url()
    message = 'Glip Bot **needs your authorization** before it can process your requests. **[Click here]('+auth_url+')** to authorize the bot.\n'
    return message

def handler(creator_id,bot_id,group_id,message,new_group=False):

    logging.info('received the message: '+ message)
    if new_group:
        #display welcome message
        return resopnse_for_new_group()
    else:
        try:
            #Send command to lex and identify intent
            print(creator_id+group_id)
            lex_response = lex_client.post_text(
                botName='GlipBot',
                botAlias='$LATEST',
                userId=creator_id+group_id,
                sessionAttributes={
                    'creator_id': creator_id,
                    'group_id': group_id
                },
                inputText=message
            )
            
            print('lex response')
            print(lex_response)
            
            if lex_response['dialogState'] == 'ElicitIntent':
                return lex_response['message']
            if lex_response['dialogState'] == 'Failed':
                return lex_response['message']
            elif lex_response['intentName'] == 'Help' and lex_response['dialogState'] == 'ReadyForFulfillment':
                #get 'FeatureGroup' slot from lex and post message
                return response_for_help(lex_response['slots']['FeatureGroup'])
            elif lex_response['intentName'] == 'Help' and lex_response['dialogState'] == 'ElicitSlot':
                #get 'FeatureGroup' slot from lex and post message
                reply_message = lex_response['message']
                reply_message = reply_message.replace('\\n','\n')
                return reply_message
            elif helper.has_valid_token(creator_id):
                if lex_response['intentName'] == 'CompanyInfo' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    company_details = helper.get('/account/~',None)
                    return rsp_for_get_company_info(company_details)
                elif lex_response['intentName'] == 'CompanyServicePlan' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    company_details = helper.get('/account/~',None)
                    return rsp_for_company_service_plan(company_details)
                elif lex_response['intentName'] == 'CompanyBillingPlan' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    company_details = helper.get('/account/~',None)
                    return rsp_for_company_service_plan(company_details)
                elif lex_response['intentName'] == 'CompanyTimeZone' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    company_details = helper.get('/account/~',None)
                    return rsp_for_company_time_zone(company_details)
                elif lex_response['intentName'] == 'CompanyGreeting' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    company_details = helper.get('/account/~',None)
                    return rsp_for_company_greeting(company_details)
            else:
                reply_message = get_auth_url_msg(creator_id,bot_id,group_id)
                return reply_message

        except Exception as error:
            logging.error(error)
            traceback.print_exc()
            #post message an error has occured while processing your request

    #if 'new group' have been created display welcome message 
    #Check if the bot has been authorized. 
    # - If it has not been authorized post auth url
    # - Else process the command

    #Process commands by sending them to Lex
    # - If intent ready for fulfillment perform intent and post message
    # - If intent needs additional parametrs post the message returned by Lex
    # - If command does not match any intent. Ask user to rephrase and post what the bot can help with.