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
                elif lex_response['intentName'] == 'PersonalInfo' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    extension_details = helper.get('/restapi/v1.0/account/~/extension/~', None)
                    return rsp_for_personal_info(extension_details)
                elif lex_response['intentName'] == 'BusinessHours' and lex_response['dialogState'] == 'ElicitSlot':
                    reply_message = lex_response['message']
                    reply_message = reply_message.replace('\\n','\n')
                    return reply_message
                elif lex_response['intentName'] == 'BusinessHours' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    if lex_response['slots']['HoursFor'] == 'personal':
                        user_business_hours = helper.get('/restapi/v1.0/account/~/extension/~/business-hours', None)
                        return rsp_for_business_hours(user_business_hours)
                    elif lex_response['slots']['HoursFor'] == 'company':
                        company_business_hours = helper.get('/restapi/v1.0/account/~/business-hours', None)
                        return rsp_for_business_hours(company_business_hours)
                elif lex_response['intentName'] == 'GetServices' and lex_response['dialogState'] == 'ElicitSlot':
                    reply_message = lex_response['message']
                    reply_message = reply_message.replace('\\n','\n')
                    return reply_message
                elif lex_response['intentName'] == 'GetServices' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    extension_details = helper.get('/restapi/v1.0/account/~/extension/~', None)
                    reply_message = rsp_for_user_services(extension_details,lex_response['slots']['ServiceType'])
                    return reply_message
                elif lex_response['intentName'] == 'CallerID' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    caller_id_details = helper.get('/restapi/v1.0/account/~/extension/~/caller-id', None)
                    reply_message = rsp_for_caller_id(caller_id_details)
                    return reply_message
                elif lex_response['intentName'] == 'EditPersonalInfo' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    reply_message = rsp_for_edit_personal_info()
                    return reply_message
                elif lex_response['intentName'] == 'PresenceInfo' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    query_params = {
                        'detailedTelephonyState': True,
                        'sipData': False
                    }
                    presence_info = helper.get('/restapi/v1.0/account/~/extension/~/presence',query_params)
                    reply_message = rsp_for_user_presence(presence_info)
                    return reply_message
                elif lex_response['intentName'] == 'EditCallerID' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    reply_message = rsp_for_edit_callerID_settings()
                    return reply_message
                elif lex_response['intentName'] == 'EditBusinessHours' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    reply_message = rsp_for_edit_user_hours()
                    return reply_message
                elif lex_response['intentName'] == 'EditUserStatus' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    update_user_status = generate_update_user_status_body(lex_response['slots']['UserStatus'])
                    helper.put('/restapi/v1.0/account/~/extension/~/presence',update_user_status)
                    return 'Successfully changed your user status to: **'+lex_response['slots']['UserStatus']+'**'
                elif lex_response['intentName'] == 'EditUserStatus' and lex_response['dialogState'] == 'ElicitSlot':
                    reply_message = lex_response['message']
                    reply_message = reply_message.replace('\\n','\n')
                    return reply_message
                elif lex_response['intentName'] == 'EditDnDStatus' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    update_dnd = generate_update_dnd_body(lex_response['slots']['DnDStatus'])
                    helper.put('/restapi/v1.0/account/~/extension/~/presence',update_dnd)
                    return 'Successfully changed your Do Not Disturb status to: **'+lex_response['slots']['DnDStatus']+'**'
                elif lex_response['intentName'] == 'EditDnDStatus' and lex_response['dialogState'] == 'ElicitSlot':
                    reply_message = lex_response['message']
                    reply_message = reply_message.replace('\\n','\n')
                    return reply_message
                elif lex_response['intentName'] == 'NotificationSettings' and lex_response['dialogState'] == 'ReadyForFulfillment':
                    nofity_details = helper.get('/account/~/extension/~/notification-settings', None)
                    return rsp_for_get_notify(nofity_details,lex_response['slots']['AlertsFor'])
                elif lex_response['intentName'] == 'NotificationSettings' and lex_response['dialogState'] == 'ElicitSlot':
                    reply_message = lex_response['message']
                    reply_message = reply_message.replace('\\n','\n')
                    return reply_message                    

            else:
                reply_message = get_auth_url_msg(creator_id,bot_id,group_id)
                return reply_message

        except Exception as error:
            logging.error(error)
            traceback.print_exc()
            return 'An error as occured while processing your request'
            #post message an error has occured while processing your request

    #if 'new group' have been created display welcome message 
    #Check if the bot has been authorized. 
    # - If it has not been authorized post auth url
    # - Else process the command

    #Process commands by sending them to Lex
    # - If intent ready for fulfillment perform intent and post message
    # - If intent needs additional parametrs post the message returned by Lex
    # - If command does not match any intent. Ask user to rephrase and post what the bot can help with.