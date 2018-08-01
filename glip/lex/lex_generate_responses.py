
grp_company_info = 'company info'
grp_personal_info = 'personal info'
grp_notification_settings = 'notification settings'
grp_presence_info = 'presence info'
grp_callerID_info = 'caller ID info'

def resopnse_for_new_group(bot_id):
    ret_val = 'Hello!! I am [:Person]('+bot_id+')!! I can help you with the following:'
    ret_val = ret_val+'* **View your company information** like billing plan, service plane, business hours etc.\n'
    ret_val = ret_val+'* **View/edit your personal information** like personal information, business hours, services available etc.\n'
    ret_val = ret_val+'* **View/edit your notification settings** for Voicemails, Texts and Fax\n'
    ret_val = ret_val+'* **View/edit your presence information** (Do Not Disturb, User Status etc.)\n'
    ret_val = ret_val+'* **View/edit your caller ID settings** for available features\n'
    ret_val = ret_val+ 'If you would like see more detailed information about any of the functions above please type \'I need help with [function name]\''
    ret_val = re_val+ 'for example if you need more details about company informations you can type \'I need more help with company information\'\nFinally,'
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
        ret_val = ret_val + '* **Edit personal greetings**\n'
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