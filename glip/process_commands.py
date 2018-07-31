from core.rc_client_helper import RCClientHelper
import logging
import re
from glip.generate_responses import *
from glip.generate_update_body import *
import traceback
import json
from ringcentral.http.api_exception import ApiException

def handler(owner_id,bot_id,group_id,command):
    #regular expressions for commands
    re_help_command = r'^help(:[ ]?(all|company info|notification settings|personal info|callerID|presence))?([ ]+)?$'
    re_get_company_commands = r'get company (info|time-zone|time zone|service plan|billing plan|greeting language)\w?'
    re_get_notify_settings = r'Get (notification|alert|notify) settings: (voicemail|voicemails|in-fax|in-text|out-fax|missed call|missed calls)\w?'
    re_put_enable_notify_settings = r'enable (email|sms) notifications for (voicemail|voicemails|in-fax|in-text|out-fax|missed call|missed calls)\w?'
    re_put_disable_notify_settings = r'disable (email|sms) notifications for (voicemail|voicemails|in-fax|in-text|out-fax|missed call|missed calls)\w?'
    re_get_personal_info = r'get my (personal info)'
    re_get_business_hours = r'get (my|company) business hours'
    re_get_user_service_info = r'get (services available|services unavailable) to me'
    re_get_caller_id_info = r'get (caller ID| callerID) settings'
    re_get_presence = r'^get presence info$'
    re_edit_personal_info = r'edit my (personal info)'
    re_edit_callerID_settings = r'edit (caller ID| callerID) settings'
    re_edit_my_business_hours = r'edit my business hours'
    re_edit_dnd_info = r'^(^Take All Calls$)|(^Do Not Accept Any Calls$)|(^Do Not Accept Department Calls$)|(^Take Department Calls Only$)$'
    re_edit_user_status = r'^Set my status to (Offline|Busy|Available)$'
    const_new_group = r'new group'
    

    print(command)
    try:
        logging.info('received the command: '+ command)
        helper = RCClientHelper()

        if re.match(const_new_group, command, flags=re.I):
            return resopnse_for_new_group()

        if re.match(re_help_command, command, flags=re.I):
            match = re.match(re_help_command, command, flags=re.I)
            return response_for_help(match.group(2))

        #If the token is valid
        if helper.has_valid_token(owner_id):
            #Process requests based on the command
            logging.info('The account '+ owner_id+' has a valid token. ')
            logging.info('Processing the command: '+ command)
            
            if re.match(re_get_company_commands, command, flags=re.I):
                company_details = helper.get('/account/~',None)
                print('received company details')
                match = re.match(re_get_company_commands, command, flags=re.I)
                return response_for_get_company(company_details, command, match.group(1))
                
            elif re.match(re_get_notify_settings, command, flags=re.I):
                nofity_details = helper.get('/account/~/extension/~/notification-settings', None)
                print('received notify details')
                match = re.match(re_get_notify_settings, command, flags=re.I)
                return response_for_get_notify(nofity_details, command, match.group(2))
            
            elif re.match(re_put_enable_notify_settings, command, flags=re.I):
                match = re.match(re_put_enable_notify_settings, command, flags=re.I)
                current_settings = helper.get('/account/~/extension/~/notification-settings', None)
                updated_settings = generate_update_notify_body(match.group(1),match.group(2),current_settings,True)
                if updated_settings != None:
                    helper.put('/account/~/extension/~/notification-settings',updated_settings)
                    return 'Successful!! you will receive **'+ match.group(1) +'** notifications for **'+ match.group(2) +'**.'
                else:
                    return 'invalid command'

            elif re.match(re_put_disable_notify_settings, command, flags=re.I):
                match = re.match(re_put_disable_notify_settings, command, flags=re.I)
                current_settings = helper.get('/account/~/extension/~/notification-settings', None)
                updated_settings = generate_update_notify_body(match.group(1),match.group(2),current_settings, False)
                if updated_settings != None:
                    helper.put('/account/~/extension/~/notification-settings',updated_settings)
                    return 'Successful!! you will **NOT** receive **'+ match.group(1) +'** notifications for **'+ match.group(2) +'**.'
                else:
                    return 'invalid command'

            elif re.match(re_get_personal_info, command, flags=re.I):
                extension_details = helper.get('/restapi/v1.0/account/~/extension/~', None)
                return response_for_personal_info(extension_details)

            elif re.match(re_get_user_service_info, command, flags=re.I):
                match = re.match(re_get_user_service_info, command, flags=re.I)
                extension_details = helper.get('/restapi/v1.0/account/~/extension/~', None)
                return response_for_user_services(extension_details,match.group(1))

            elif re.match(re_get_caller_id_info, command, flags=re.I):
                caller_id_details = helper.get('/restapi/v1.0/account/~/extension/~/caller-id', None)
                return response_for_caller_id(caller_id_details)

            elif re.match(re_edit_personal_info, command, flags=re.I):
                return response_for_edit_personal_info()

            elif re.match(re_edit_callerID_settings, command, flags=re.I):
                return response_for_edit_callerID_settings()
            
            elif re.match(re_get_business_hours, command, flags=re.I):
                match = re.match(re_get_business_hours, command, flags=re.I)
                if match.group(1) == 'my':
                    user_business_hours = helper.get('/restapi/v1.0/account/~/extension/~/business-hours', None)
                    return response_for_business_hours(user_business_hours)
                elif match.group(1) == 'company':
                    company_business_hours = helper.get('/restapi/v1.0/account/~/business-hours', None)
                    return response_for_business_hours(user_business_hours)

            elif re.match(re_edit_my_business_hours, command, flags=re.I):
                return response_for_edit_user_hours()
            
            elif re.match(re_get_presence, command, flags=re.I):
                query_params = {
                    'detailedTelephonyState': True,
                    'sipData': False
                }
                presence_info = helper.get('/restapi/v1.0/account/~/extension/~/presence',query_params)
                print(presence_info)
                return response_for_user_presence(presence_info)

            elif re.match(re_edit_dnd_info, command, flags=re.I):
                match = re.match(re_edit_dnd_info, command, flags=re.I)
                if match.group(1) != None:
                    update_dnd = generate_update_dnd_body('TakeAllCalls')
                    helper.put('/restapi/v1.0/account/~/extension/~/presence',update_dnd)
                    return 'Successfully changed your Do Not Disturb status to: **'+match.group(1)+'**'
                elif match.group(2) != None:
                    update_dnd = generate_update_dnd_body('DoNotAcceptAnyCalls')
                    helper.put('/restapi/v1.0/account/~/extension/~/presence',update_dnd)
                    return 'Successfully changed your Do Not Disturb status to: **'+match.group(2)+'**'
                elif match.group(3) != None:
                    update_dnd = generate_update_dnd_body('DoNotAcceptDepartmentCalls')
                    helper.put('/restapi/v1.0/account/~/extension/~/presence',update_dnd)
                    return 'Successfully changed your Do Not Disturb status to: **'+match.group(3)+'**'
                else:
                    update_dnd = generate_update_dnd_body('TakeDepartmentCallsOnly')
                    helper.put('/restapi/v1.0/account/~/extension/~/presence',update_dnd)
                    return 'Successfully changed your Do Not Disturb status to: **'+match.group(4)+'**'
            elif re.match(re_edit_user_status, command, flags=re.I):
                match = re.match(re_edit_user_status, command, flags=re.I)
                status = match.group(1)
                status=status.capitalize()
                update_user_status = generate_update_user_status_body(status)
                helper.put('/restapi/v1.0/account/~/extension/~/presence',update_user_status)
                return 'Successfully changed your status to: **'+status+'**'
            
            message = "Received command: "+command
            #message = response_test()
            return message
        else:
            #Save account ID, botID and groupID to the table
            #Get and post auth url
            helper.save_bot_and_group_id(owner_id, bot_id, group_id)
            auth_url = helper.get_auth_url()
            message = 'Glip Bot does not have the authorization to execute this command. [Click here]('+auth_url+') to authorize.\n'
            return message
    except ApiException as error:
        logging.error(error)
        error_response = error.api_response().json_dict()
        print(error_response) 
        traceback.print_exc()

        if error_response['errorCode'] ==  'CMN-408':
            return 'You need **'+error_response['permissionName']+'** to execute this command'
        elif error_response['errorCode'] ==  'PRS-101':
            return error_response['message']
        else:
            return 'An error occurred while processing your request'