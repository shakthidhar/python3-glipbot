import json
import logging
import os
import time
import uuid
from urllib.parse import parse_qs
from glip.bot_request_handler import handler as bot_handler
from glip.helper_request_handler import handler as helper_handler

logger = logging.getLogger('api')
logger.setLevel(logging.INFO)


def handler(event, context):

    if 'bot' in event:
        print(event['bot'])
        return 
    else:
        #Get path parameters from event
        service = event['pathParameters']['service']
        request_type = event['pathParameters']['request_type']
        if service == 'bot':
            return bot_handler(event)
        elif service == 'helper':
            return helper_handler(event)
        else:
            response = {
                "statusCode": 400,
                "body": "Invalid request"
            }
            return response