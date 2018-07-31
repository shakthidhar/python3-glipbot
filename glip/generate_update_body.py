

def generate_update_dnd_body(dnd_status):
    ret_val = {
        #'userStatus':presence_info['userStatus'],
        'dndStatus':dnd_status,
        #'message':presence_info['message'],
        #'allowSeeMyPresence':presence_info['allowSeeMyPresence'],
        #'ringOnMonitoredCall':presence_info['ringOnMonitoredCall'],
        #'pickUpCallsOnHold':presence_info['pickUpCallsOnHold']
    }

    return ret_val

def generate_update_user_status_body(user_status):
    ret_val = {
        'userStatus':user_status
    }

    return ret_val

def generate_update_notify_body(notify_on,notification_for, current_settings, enable):
    if enable:
        setting = 'True'
    else:
        setting = 'False'
    if notification_for.lower() == 'voicemail' or notification_for.lower() == 'voicemails':
        if notify_on.lower() == 'email':
            current_settings['voicemails']['notifyByEmail'] = setting
            return current_settings
        elif notify_on.lower() == 'sms':
            current_settings['voicemails']['notifyBySms'] = setting
            return current_settings
        else:
            return None
    if notification_for.lower() == 'in-fax':
        if notify_on.lower() == 'email':
            current_settings['inboundFaxes']['notifyByEmail'] = setting
            return current_settings
        elif notify_on.lower() == 'sms':
            current_settings['inboundFaxes']['notifyBySms'] = setting
            return current_settings
        else:
            return None
    if notification_for.lower() == 'out-fax':
        if notify_on.lower() == 'email':
            current_settings['outboundFaxes']['notifyByEmail'] = setting
            return current_settings
        elif notify_on.lower() == 'sms':
            current_settings['outboundFaxes']['notifyBySms'] = setting
            return current_settings
        else:
            return None
    if notification_for.lower() == 'in-text':
        if notify_on.lower() == 'email':
            current_settings['inboundTexts']['notifyByEmail'] = setting
            return current_settings
        elif notify_on.lower() == 'sms':
            current_settings['inboundTexts']['notifyBySms'] = setting
            return current_settings
        else:
            return None
    if notification_for.lower() == 'missed call' or notification_for.lower() == 'missed calls':
        if notify_on.lower() == 'email':
            current_settings['missedCalls']['notifyByEmail'] = setting
            return current_settings
        elif notify_on.lower() == 'sms':
            current_settings['missedCalls']['notifyBySms'] = setting
            return current_settings
        else:
            return None
            