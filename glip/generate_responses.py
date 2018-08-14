#The functions in this file are no longer used. All generate responses request are sent to lex_generate_responses 
import re

command_groups = '* **help: company info** - to list commands for viewing Company Information\n'
command_groups = command_groups + '* **help: notification settings** - to list commands to view/update Notification Settings \n'
command_groups = command_groups + '* **help: personal info** -  to list commands to view/update Personal Infomation\n'
command_groups = command_groups + '* **help: callerID** - to list commands to view/update Caller ID Settings\n'
command_groups = command_groups + '* **help: presence** - to list commands to view/update Caller ID Settings\n'
command_groups = command_groups + '* **help: all** - to view all commands\n'

company_commands = '* **Get company info** - to view company id, name, main number and operator extension\n'
company_commands = company_commands + '* **Get company billing plan** - to view billing id, name, duration unit, duration, type and included phone lines\n'
company_commands = company_commands + '* **Get company service plan** - to view service ID, name and service edition\n'
company_commands = company_commands + '* **Get company time-zone** - to view time-zone ID, name, description and bias\n'
company_commands = company_commands + '* **Get company greeting language** - to view greeting language, name and local code\n'
company_commands = company_commands + '* **Get company business hours** - to view greetin ID, name and local code\n'

notification_commands = '* **Get notification settings: [feature]** - to view the notification settings for a given feature\n'
notification_commands = notification_commands + '* **Enable [platform] notifications for [feature]** - to receive notifications on a platform for a given feature\n'
notification_commands = notification_commands + '* **Disable [platform] notifications for [feature]** - to receive notifications on a platform for a given feature\n'
notification_commands = notification_commands + 'For the above commands **[platform]** can take values **email** and **sms**.'
notification_commands = notification_commands + ' **[feature]** can take values **voicemails**, **missed calls**, **in-fax**, **out-fax** and **in-text**. '

presence_commands = '* **Get presence info** - to view your presence info\n'
presence_commands = presence_commands +'* **Take all calls** - to change your Do Not Disturb status to Take all calls\n'
presence_commands = presence_commands +'* **Do not accept any calls** - to change your Do Not Disturb status to decline all calls\n'
presence_commands = presence_commands +'* **Set my status to [Available|Busy|Offline]** - to change your user status to Available, Busy or Offline\n'

caller_id_commands = '* **Get caller ID settings** - to view your caller ID settings for available features\n'
caller_id_commands = caller_id_commands +'* **Edit caller ID settings** - to edit your caller ID settings for available features\n'

personal_commands = '* **Get my personal info** - to view your personal information including your business address and phone number\n'
personal_commands = personal_commands + '* **Get my business hours** - to view your business hours\n'
personal_commands = personal_commands + '* **Edit my business hours** - to edit your business hours\n'
personal_commands = personal_commands + '* **Get services available to me** - to view all the RingCentral services that available for you to use\n'
personal_commands = personal_commands + '* **Get services unavailable to me** - to view all the RingCentral services that are not available for you\n'
personal_commands = personal_commands + '* **Edit my personal information** - to edit you personal infomation\n'
personal_commands = personal_commands + '* **Edit personal greetings** - to edit your personal greetings\n'

service_web_settings_url = 'https://service.ringcentral.com/application/settings/'

def response_test():
    ret_val = {
        "text": "",
        "attachments": [{
            "type": "Card",
            "fallback": "The attachment isn't supported.",
            "color": "#9C1A22",
            "fields": [{
            "title": "Company ID",
            "value": "1210",
            "style": "Long"
            },
            {
                "title": "Company Name",
                "value": "RingCentral",
                "style": "Long"
            },
            {
                "title": "Main Number",
                "value": "+14158021958",
                "style": "Long"
            },
            {
                "title": "Operator Extension",
                "value": "101",
                "style": "Long"
            },
            {
                "title": " Company Home Country",
                "value": "United States",
                "style": "Long"
            }
            ],
        }
        ]
    }
    return ret_val

def response_for_user_presence(presence_info):
    presence_status = presence_info['presenceStatus']
    telephony_status = presence_info['telephonyStatus']
    user_status = presence_info['userStatus']
    dnd_status = presence_info['dndStatus']
    ring_on_monitored_call = presence_info['ringOnMonitoredCall']
    pick_up_calls_on_hold = presence_info['pickUpCallsOnHold']

    ret_val = '**Presence Status**: {presence_status}\n'.format(presence_status=presence_status)
    ret_val = ret_val + '**Telephony Status**: {telephony_status}\n'.format(telephony_status=telephony_status)
    ret_val = ret_val + '**User Status**: {user_status}\n'.format(user_status=user_status)
    ret_val = ret_val + '**Do Not Disturb Status**: {dnd_status}\n'.format(dnd_status=dnd_status)
    ret_val = ret_val + '**Ring On Monitored Call**: {ring_on_monitored_call}\n'.format(ring_on_monitored_call=ring_on_monitored_call)
    ret_val = ret_val + '**Pick Up Calls On Hold**: {pick_up_calls_on_hold}\n'.format(pick_up_calls_on_hold=pick_up_calls_on_hold)
    return ret_val


def response_for_business_hours(business_hours_info):
    ret_val = '|**Day**|**From**|**To**|\n'
    schedule = business_hours_info['schedule']
    if bool(schedule):
        weekly_range = schedule['weeklyRanges']
        if 'monday' in weekly_range:
            ret_val = ret_val+'|Monday|'+weekly_range['monday'][0]['from']+'|'+weekly_range['monday'][0]['to']+'|\n'
        if 'tuesday' in weekly_range:
            ret_val = ret_val+'|Tuesday|'+weekly_range['tuesday'][0]['from']+'|'+weekly_range['tuesday'][0]['to']+'|\n'
        if 'wednesday' in weekly_range:
            ret_val = ret_val+'|Wednesday|'+weekly_range['wednesday'][0]['from']+'|'+weekly_range['wednesday'][0]['to']+'|\n'
        if 'thursday' in weekly_range:
            ret_val = ret_val+'|Thursday|'+weekly_range['thursday'][0]['from']+'|'+weekly_range['thursday'][0]['to']+'|\n'
        if 'friday' in weekly_range:
            ret_val = ret_val+'|Friday|'+weekly_range['friday'][0]['from']+'|'+weekly_range['friday'][0]['to']+'|\n'
        if 'saturday' in weekly_range:
            ret_val = ret_val+'|Saturday|'+weekly_range['saturday'][0]['from']+'|'+weekly_range['saturday'][0]['to']+'|\n'
        if 'sunday' in weekly_range:
            ret_val = ret_val+'|Sunday|'+weekly_range['sunday'][0]['from']+'|'+weekly_range['sunday'][0]['to']+'|\n'
        return ret_val
    else:
        return 'Available 24 hours/7 days a week'

def response_for_edit_user_hours():
    ret_val = '[Click here]'+'('+service_web_settings_url+'settings/extensionInfo/settingsAndPermissions' +') to edit your bussiness hours.'
    return ret_val

def response_for_edit_personal_info():
    ret_val = '[Click here]'+'('+service_web_settings_url+'settings/extensionInfo/general' +') to edit your personal information.'
    return ret_val

def response_for_edit_callerID_settings():
    ret_val = '[Click here]'+'('+service_web_settings_url+'outboundCallsFaxes/callerId' +') to edit your caller ID information.'
    return ret_val

def resopnse_for_new_group():
    ret_val = 'Hello!! I am Glip Bot!! I can help you view/edit your: company info, notification settings, personal info and caller ID Settings.'
    ret_val = ret_val + ' Here is a list of commands to help you get started:\n'
    ret_val = ret_val + command_groups
    ret_val = ret_val + 'Finally, type **help** to view this message.'
    return ret_val

def response_for_help(query):
    if query == None:
        ret_val = "Here is a list of things I can help you with:\n"
        ret_val = ret_val + command_groups
        ret_val = ret_val + 'Finally, type **help** to view this message.'
        return ret_val
    elif query.lower() == 'company info':
        ret_val = "Here is a list of commands to view company information:\n"
        ret_val = ret_val + company_commands
        ret_val = ret_val + 'Finally, type **help** to list the things Glip Bot can help you with'
        return ret_val
    elif query.lower() == 'notification settings':
        ret_val = "Here is a list of commands to view/edit your notification settings:\n"
        ret_val = ret_val + notification_commands
        ret_val = ret_val + 'Finally, type **help** to list the things Glip Bot can help you with'
        return ret_val
    elif query.lower() == 'personal info':
        ret_val = "Here is a list of commands to view/edit your personal information:\n"
        ret_val = ret_val + personal_commands
        ret_val = ret_val + 'Finally, type **help** to list the things Glip Bot can help you with'
        return ret_val
    elif query.lower() == 'callerid':
        ret_val = "Here is a list of commands to view/edit your caller ID settings:\n"
        ret_val = ret_val + caller_id_commands
        ret_val = ret_val + 'Finally, type **help** to list the things Glip Bot can help you with'
        return ret_val
    elif query.lower() == 'presence':
        ret_val = "Here is a list of commands to view/edit your presence information:\n"
        ret_val = ret_val + presence_commands
        ret_val = ret_val + 'Finally, type **help** to list the things Glip Bot can help you with'
        return ret_val
    elif query.lower() == 'all':
        return 'Working on it'

def response_for_personal_info(extension_details):
    #print('extension details')
    #print(extension_details)
    ret_val = '**First Name**: {first_name}\n**Last Name**: {last_name}\n**Email**: {email}\n'.format(
        first_name = extension_details['contact']['firstName'],
        last_name = extension_details['contact']['lastName'],
        email = extension_details['contact']['email']
    )
    if 'company' in extension_details['contact']:
        ret_val = ret_val + '**Company**: {company}'.format(company = extension_details['contact']['company'])
    if 'businessPhone' in extension_details['contact']:
        ret_val = ret_val + '**Bussiness Phone**: {business_phone}\n'.format(business_phone = extension_details['contact']['businessPhone'])
    if 'extensionNumber' in extension_details:
        ret_val = ret_val + '**Extension Number**: {extension_number}\n'.format(extension_number = extension_details['extensionNumber'])
    if 'businessAddress' in extension_details['contact']:
        ret_val = ret_val + '**Address**: {address}'.format(
            address = extension_details['contact']['businessAddress']['street']+'\n\t'
            +extension_details['contact']['businessAddress']['city']+', '+extension_details['contact']['businessAddress']['state']+'\n\t'
            +extension_details['contact']['businessAddress']['country']+' '+extension_details['contact']['businessAddress']['zip']
        )
    print('generated message for contact information' + ret_val)
    return ret_val

def response_for_user_services(extension_details, query):
    feature_list = extension_details['serviceFeatures']
    ret_val = ''
    if query.lower() == 'services available':
        count = 0
        for i in range(len(feature_list)):
            if count == 0 and feature_list[i]['enabled']:
                ret_val = ret_val + feature_list[i]['featureName']
                count = 1
            elif feature_list[i]['enabled']:
                ret_val = ret_val +', '+ feature_list[i]['featureName']
        return ret_val
    elif query.lower() == 'services unavailable':
        ret_val = '|**Feature Name**|**Reason**|\n'
        for i in range(len(feature_list)):
            if not feature_list[i]['enabled']:
                ret_val = ret_val + '|'+feature_list[i]['featureName']+'|'+feature_list[i]['reason']+'|\n'
        return ret_val

def response_for_caller_id(caller_id_details):
    caller_id_by_feature = caller_id_details['byFeature']
    ret_val = '|**Feature**|**Caller ID Type**|**Phone Number**|\n'
    for i in range(len(caller_id_by_feature)):
        feature = caller_id_by_feature[i]['feature']
        callerId = caller_id_by_feature[i]['callerId']
        if bool(callerId):
            ret_val = ret_val + '|'+ feature +'|'+ callerId['type']+'|'
            if callerId['type'] == "PhoneNumber":
                ret_val = ret_val+callerId['phoneInfo']['phoneNumber']+'|\n'
            else:
                ret_val = ret_val+'| |\n'
    return ret_val


def response_for_get_notify(nofity_details, command, query):
    if query.lower() == 'voicemail' or query.lower() == 'voicemails':
        ret_val ='**Notify by Email**: {email_notify}\n**Notify by SMS**: {sms_notify}\n**Include Attachment**: {attachment_ststus}\n**Mark as Read**: {read_status}'.format(
            email_notify=nofity_details['voicemails']['notifyByEmail'],
            sms_notify=nofity_details['voicemails']['notifyBySms'],
            attachment_ststus=nofity_details['voicemails']['includeAttachment'],
            read_status=nofity_details['voicemails']['markAsRead']
        )
        print('generated message for voicemail notification settings:' + ret_val)
        return ret_val
    elif query.lower() == 'in-fax':
        ret_val ='**Notify by Email**: {email_notify}\n**Notify by SMS**: {sms_notify}\n**Include Attachment**: {attachment_ststus}\n**Mark as Read**: {read_status}'.format(
            email_notify=nofity_details['inboundFaxes']['notifyByEmail'],
            sms_notify=nofity_details['inboundFaxes']['notifyBySms'],
            attachment_ststus=nofity_details['inboundFaxes']['includeAttachment'],
            read_status=nofity_details['inboundFaxes']['markAsRead']
        )
        print('generated message for voicemail notification settings:' + ret_val)
        return ret_val
    elif query.lower() == 'out-fax':
        ret_val ='**Notify by Email**: {email_notify}\n**Notify by SMS**: {sms_notify}'.format(
            email_notify=nofity_details['outboundFaxes']['notifyByEmail'],
            sms_notify=nofity_details['outboundFaxes']['notifyBySms']
        )
        print('generated message for coicemail notification settings:' + ret_val)
        return ret_val
    elif query.lower() == 'in-text':
        ret_val ='**Notify by Email**: {email_notify}\n**Notify by SMS**: {sms_notify}'.format(
            email_notify=nofity_details['inboundTexts']['notifyByEmail'],
            sms_notify=nofity_details['inboundTexts']['notifyBySms']
        )
        print('generated message for coicemail notification settings:' + ret_val)
        return ret_val
    elif query.lower() == 'missed call' or query.lower() == 'missed calls':
        ret_val ='**Notify by Email**: {email_notify}\n**Notify by SMS**: {sms_notify}'.format(
            email_notify=nofity_details['missedCalls']['notifyByEmail'],
            sms_notify=nofity_details['missedCalls']['notifyBySms']
        )
        print('generated message for coicemail notification settings:' + ret_val)
        return ret_val
    else:
        return 'Invalid Command'

def response_for_get_company(company_details, command, query):
    if query.lower() == 'info':
        ret_val = '**Company ID**: {company_id}\n**Company Name**: {brand_name}\n**Main Number**: {main_number}\n**Operator Extension**: {operator_extension}\n**Company Home Country**: {home_country}'.format(
            company_id=company_details['serviceInfo']['brand']['id'],
            brand_name=company_details['serviceInfo']['brand']['name'],
            main_number=company_details['mainNumber'],
            operator_extension=company_details['operator']['extensionNumber'],
            home_country=company_details['serviceInfo']['brand']['homeCountry']['name']
        )
        print('generated message for company info: '+ ret_val)
        return ret_val
    elif query.lower() == 'service plan':
        ret_val = '**Service ID**: {service_id}\n**Service Name**: {service_name}\n**Service edition**: {service_number}'.format(
            service_id=company_details['serviceInfo']['servicePlan']['id'],
            service_name=company_details['serviceInfo']['servicePlan']['name'],
            service_number=company_details['serviceInfo']['servicePlan']['edition']
        )
        print('generated message company service plan: '+ ret_val)
        return ret_val
    elif query.lower() == 'billing plan':
        ret_val = '**Billing ID**: {billing_id}\n**Billing Name**: {billing_name}\n**Duration Unit**: {duration_unit}\n**Duration**: {duration}\n**Type**: {type}\n**Included Phone Lines**: {phone_lines}'.format(
            billing_id=company_details['serviceInfo']['billingPlan']['id'],
            billing_name=company_details['serviceInfo']['billingPlan']['name'],
            duration_unit=company_details['serviceInfo']['billingPlan']['durationUnit'],
            duration=company_details['serviceInfo']['billingPlan']['duration'],
            type=company_details['serviceInfo']['billingPlan']['type'],
            phone_lines=company_details['serviceInfo']['billingPlan']['includedPhoneLines']
        )
        print('generated message company billing plan: '+ ret_val)
        return ret_val
    elif query.lower() == 'time zone' or query.lower() == 'time-zone':
        ret_val = '**ID**: {id}\n**Name**: {name}\n**Description**: {description}\n**Bias**: {bias}'.format(
            id=company_details['regionalSettings']['timezone']['id'],
            name=company_details['regionalSettings']['timezone']['name'],
            description=company_details['regionalSettings']['timezone']['description'],
            bias=company_details['regionalSettings']['timezone']['bias']
        )
        print('generated message company time zone: '+ ret_val)
        return ret_val
    elif query.lower() == 'greeting language':
        ret_val = '**ID**: {id}\n**Name**: {name}\n**Locale Code**: {locale_code}'.format(
            id=company_details['regionalSettings']['greetingLanguage']['id'],
            name=company_details['regionalSettings']['greetingLanguage']['name'],
            locale_code=company_details['regionalSettings']['greetingLanguage']['localeCode']
        )
        print('generated message company greeting language: '+ ret_val)
        return ret_val
    else:
        return 'Invalid Command'
        