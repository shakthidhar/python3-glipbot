grp_company_info = 'company info'
grp_personal_info = 'personal info'
grp_notification_settings = 'notification settings'
grp_presence_info = 'presence info'
grp_callerID_info = 'caller ID info'

service_web_settings_url = 'https://service.ringcentral.com/application/settings/'

def response_for_new_group(creator_id, bot_id):
    ret_val = 'Hello ![:Person]('+ creator_id +')!! I am ![:Person]('+bot_id+')!! I can help you with the following:\n'
    ret_val = ret_val+'* **View your company information** like billing plan, service plane, business hours etc.\n'
    ret_val = ret_val+'* **View/edit your personal information** like personal information, business hours, services available etc.\n'
    ret_val = ret_val+'* **View/edit your notification settings** for Voicemails, Texts and Fax\n'
    ret_val = ret_val+'* **View your presence information and Edit Do Not Disturb and User Status**\n'
    ret_val = ret_val+'* **View/edit your caller ID settings** for available features\n'
    ret_val = ret_val+ 'If you would like see more detailed information about any of the functions above, please ask.'
    #ret_val = ret_val+ 'for example if you need more details about company informations you can type \'I need more help with company information\'\n'
    return ret_val

def response_for_help(function_group):
    if function_group == grp_company_info:
        ret_val = 'Here is a list of features available for **company information**:\n'
        ret_val = ret_val + '* **View company details** - company id, name, main number and operator extension\n'
        ret_val = ret_val + '* **View company billing plan** - billing id, name, duration unit, duration, type and included phone lines\n'
        ret_val = ret_val + '* **View company service plan** - service ID, name and service edition\n'
        ret_val = ret_val + '* **View company business hours** - operation hours for the entire week\n'
        ret_val = ret_val + '* **View company greeting language** - greeting language, name and local code\n'
        ret_val = ret_val + '* **View company time-zone** - time-zone ID, name, description and bias\n'
        ret_val = ret_val + 'You always ask for help to view all the other available functions'
        return ret_val
    elif function_group == grp_personal_info:
        ret_val = 'Here is a list of features available for **personal info**:\n'
        ret_val = ret_val + '* **View your personal information** - First and Last Name, Company, Business Phone and Business Hours\n'
        ret_val = ret_val + '* **View business hours** - your business hours for the entire week\n'
        ret_val = ret_val + '* **Edit my business hours**\n'
        ret_val = ret_val + '* **Services available to you** - lists all the RingCentral services that available for you to use\n'
        ret_val = ret_val + '* **Services unavailable to me** - lists all the RingCentral services that are not available for you\n'
        ret_val = ret_val + '* **Edit your personal information** - you can edit your First and Last Name, Business Phone, Business Hourss and Address\n'
        #ret_val = ret_val + '* **Edit personal greetings**\n'
        ret_val = ret_val + 'You always ask for help to view all the other available functions'
        return ret_val
    elif function_group == grp_notification_settings:
        ret_val = 'Here is a list of features available for **notification settings**:\n'
        ret_val = ret_val + '* **View notifications settings** for voicemails, missed calls, fax and texts\n'
        ret_val = ret_val + '* **Enable/Disable email or sms notifications** for voicemails, missed calls, fax and texts\n'
        ret_val = ret_val + 'You always ask for help to view all the other available functions'
        return ret_val
    elif function_group == grp_presence_info:
        ret_val = 'Here is a list of features available for **presence info**:\n'
        ret_val = ret_val + '* **View your presence info** - lists your Presence, Telephony, User and Do Not Disturb status\n'
        ret_val = ret_val + '* **Change your Do Not Disturb status ** to take all calls or to not accept any calls\n'
        ret_val = ret_val + '* **Set your user status** to Available, Busy or Offline\n'
        ret_val = ret_val + 'You always ask for help to view all the other available functions'
        return ret_val
    elif function_group == grp_callerID_info:
        ret_val = 'Here is a list of features available for **Caller ID settings**:\n'
        ret_val = ret_val + '* **View your caller ID settings** for available features\n'
        ret_val = ret_val + '* **Edit caller ID settings**\n'
        ret_val = ret_val + 'You always ask for help to view all the other available functions'
        return ret_val

def rsp_for_get_company_info(company_details):
    ret_val = '**Company ID**: {company_id}\n**Company Name**: {brand_name}\n**Main Number**: {main_number}\n**Operator Extension**: {operator_extension}\n**Company Home Country**: {home_country}'.format(
        company_id=company_details['serviceInfo']['brand']['id'],
        brand_name=company_details['serviceInfo']['brand']['name'],
        main_number=company_details['mainNumber'],
        operator_extension=company_details['operator']['extensionNumber'],
        home_country=company_details['serviceInfo']['brand']['homeCountry']['name']
    )
    print('generated message for company info: '+ ret_val)
    return ret_val

def rsp_for_company_service_plan(company_details):
    ret_val = '**Service ID**: {service_id}\n**Service Name**: {service_name}\n**Service edition**: {service_number}'.format(
        service_id=company_details['serviceInfo']['servicePlan']['id'],
        service_name=company_details['serviceInfo']['servicePlan']['name'],
        service_number=company_details['serviceInfo']['servicePlan']['edition']
    )
    print('generated message company service plan: '+ ret_val)
    return ret_val

def rsp_for_company_billing_plan(company_details):
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

def rsp_for_company_time_zone(company_details):
    ret_val = '**ID**: {id}\n**Name**: {name}\n**Description**: {description}\n**Bias**: {bias}'.format(
        id=company_details['regionalSettings']['timezone']['id'],
        name=company_details['regionalSettings']['timezone']['name'],
        description=company_details['regionalSettings']['timezone']['description'],
        bias=company_details['regionalSettings']['timezone']['bias']
    )
    print('generated message company time zone: '+ ret_val)
    return ret_val

def rsp_for_company_greeting(company_details):
    ret_val = '**ID**: {id}\n**Name**: {name}\n**Locale Code**: {locale_code}'.format(
        id=company_details['regionalSettings']['greetingLanguage']['id'],
        name=company_details['regionalSettings']['greetingLanguage']['name'],
        locale_code=company_details['regionalSettings']['greetingLanguage']['localeCode']
    )
    print('generated message company greeting language: '+ ret_val)
    return ret_val

def rsp_for_personal_info(extension_details):
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

def rsp_for_business_hours(business_hours_info):
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

def rsp_for_user_services(extension_details, query):
    feature_list = extension_details['serviceFeatures']
    ret_val = ''
    if query == 'available':
        count = 0
        for i in range(len(feature_list)):
            if count == 0 and feature_list[i]['enabled']:
                ret_val = ret_val + feature_list[i]['featureName']
                count = 1
            elif feature_list[i]['enabled']:
                ret_val = ret_val +', '+ feature_list[i]['featureName']
        return ret_val
    elif query== 'unavailable':
        ret_val = '|**Feature Name**|**Reason**|\n'
        for i in range(len(feature_list)):
            if not feature_list[i]['enabled']:
                ret_val = ret_val + '|'+feature_list[i]['featureName']+'|'+feature_list[i]['reason']+'|\n'
        return ret_val

def rsp_for_caller_id(caller_id_details):
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

def rsp_for_edit_personal_info():
    ret_val = '[Click here]'+'('+service_web_settings_url+'settings/extensionInfo/general' +') to edit your personal information.'
    return ret_val

def rsp_for_edit_callerID_settings():
    ret_val = '[Click here]'+'('+service_web_settings_url+'outboundCallsFaxes/callerId' +') to edit your caller ID information.'
    return ret_val

def rsp_for_edit_user_hours():
    ret_val = '[Click here]'+'('+service_web_settings_url+'settings/extensionInfo/settingsAndPermissions' +') to edit your bussiness hours.'
    return ret_val

def rsp_for_user_presence(presence_info):
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

def rsp_for_get_notify(nofity_details, query):
    if query.lower() == 'voicemail':
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
    elif query.lower() == 'missed call':
        ret_val ='**Notify by Email**: {email_notify}\n**Notify by SMS**: {sms_notify}'.format(
            email_notify=nofity_details['missedCalls']['notifyByEmail'],
            sms_notify=nofity_details['missedCalls']['notifyBySms']
        )
        print('generated message for coicemail notification settings:' + ret_val)
        return ret_val
    else:
        return 'Invalid Command'