
import boto3

new_group_cmd = 'new group'
help_intent = 'Help'

def handler(creator_id,group_id,command):
    
    if command == new_group_cmd:
        #display welcome message
    else:
        #Send command to lex and identify intent
        lex_response = lex_client.post_text(
            botName='GlipBot',
            botAlias='$LATEST',
            userId=creator_id+group_id,
            sessionAttributes={
                'creator_id': creator_id,
                'group_id': group_id
            },
            inputText=command
        )
        print('lex response')
        print(lex_response)
        
        if lex_response['dialogState'] == 'ElicitIntent':
            pass
            #Display the list of things the bot can help with
        if lex_response['dialogState'] == 'Failed':
            pass
            #ask user to start over
        elif lex_response['intentName'] == 'Help' and lex_response['dialogState'] == 'ReadyForFulfillment':
            pass
            #get 'FeatureGroup' slot from alots and post message

    #if 'new group' have been created display welcome message 
    #Check if the bot has been authorized. 
    # - If it has not been authorized post auth url
    # - Else process the command

    #Process commands by sending them to Lex
    # - If intent ready for fulfillment perform intent and post message
    # - If intent needs additional parametrs post the message returned by Lex
    # - If command does not match any intent. Ask user to rephrase and post what the bot can help with.