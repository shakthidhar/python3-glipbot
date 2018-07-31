from core.rc_client_helper import RCClientHelper
from core.rc_client_bot import RCClientBot
import logging

def handler(event):

    request_type = event['pathParameters']['request_type']
    rcclient_helper = RCClientHelper()
    rcclient_bot = RCClientBot()

    if request_type == 'oauth':
        print(event['queryStringParameters'])
        code = event['queryStringParameters']['code']
        try:
            rcclient_helper.auth_with_code(code)
            #get groupID and botId from the table
            #Save access token, refresh token etc to the existing table. 
            bot_info = rcclient_helper.save_token()
            response_body = get_success_page()
            
            #Post success message to glip group and send response
            response = {
                "statusCode":200,
                "headers": {"Content-Type": "text/html"},
                "body": response_body
            }
            rcclient_bot.post_message(bot_info['bot_id'], bot_info['group_id'], 'Authorization successful!!')
            return response
        except Exception as error:
            logging.error(error)
            response_body = get_error_page()
            response = {
                "statusCode":500,
                "headers": {"Content-Type": "text/html"},
                "body": response_body
            }
            return response
        
    response = {
        "statusCode": 500,
        "body": "Invalid request"
    }
    return response

def get_error_page():
    ret_val = '''
    <html>

        <head>
            <title>Android Play Store Study</title>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb"
                crossorigin="anonymous">

        </head>

        <body>
            <div class="container">
                <div class="container row align-items-center justify-content-md-center" style="width:100%; height:100%">
                    <div class="col col-md-auto justify-content-center">
                        <h3 style="text-align:center">Authorization Failed!! An error occurred while processing your request</h3>
                    </div>
                </div>
            </div>
        </body>


        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh"
            crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ"
            crossorigin="anonymous"></script>
    </html>
    '''

def get_success_page():
    ret_val = '''
    <html>

        <head>
            <title>Android Play Store Study</title>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css" integrity="sha384-PsH8R72JQ3SOdhVi3uxftmaW6Vc51MKb0q5P2rRUpPvrszuE4W1povHYgTpBfshb"
                crossorigin="anonymous">

        </head>

        <body>
            <div class="container">
                <div class="container row align-items-center justify-content-md-center" style="width:100%; height:100%">
                    <div class="col col-md-auto justify-content-center">
                        <h3 style="text-align:center">Authorization Successful!! Please return to your GlipBot</h3>
                    </div>
                </div>
            </div>
        </body>


        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
            crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.3/umd/popper.min.js" integrity="sha384-vFJXuSJphROIrBnz7yo7oB41mKfc8JzQZiCq4NCceLEaO4IHwicKwpJf9c9IpFgh"
            crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.2/js/bootstrap.min.js" integrity="sha384-alpBpkh1PFOepccYVYDB4do5UnbKysX5WZXm3XxPqe5iKTfUKjNkCk9SaVuEZflJ"
            crossorigin="anonymous"></script>
    
    </html>
    '''
    return ret_val
    