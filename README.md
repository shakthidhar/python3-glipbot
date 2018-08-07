# python3-glipbot

### Create RingCentral Apps ###
In order to build a bot that has the ability to change your ringcentral setting you are required to have two ringcentral apps:
* GlipBot
* GlipHelper

GlipBot is used to subscribe for glip events and posts. So that whenever a message is posted on Glip you receive a POST notification. The bot will also receive notifications Glip groups and bot create/remove events.
```
#Get Glip Post Events
"/restapi/v1.0/glip/posts"
#Get Glip Group Events
"/restapi/v1.0/glip/groups"
#Get Bot Create/Remove events
"/restapi/v1.0/account/~/extension/~"
```
Create the GlipBot application using your ringcentral developer account. Set Platform Type to Server/Bot and give it give it the following permissions: Glip, Read Accounts, Webhook Subscription.

Since GlipBot is of the type 'Server/Bot' its extension does not have the permissions to necessary to read and edit users' ringcentral settings. Therefore, we create another application, GlipHelper, to handle this.

For the GlipHelper application, set the Platform Type to Server/Web and provide it with the following permissions: Edit Extensions, Edit Messages, Edit Presence, Read Accounts, Read Contacts and Read Messages.

### Update Serverless-template.yml file ###
Populate the environment variables in the serverless-template.yml file and rename it serverless.yml

```
environment:
    RINGCENTRAL_ENV: https://platform.ringcentral.com
    BOT_CLIENT_ID: replace-with-bot-client-ID
    BOT_CLIENT_SECRET: replace-with-bot-client-secret
    REDIRECT_HOST: replace-with-url-from-aws-gateway-api
    HELPER_CLIENT_ID: replace-with-helper-client-ID
    HELPER_CLIENT_SECRET: replace-with-helper-client-secret
    BOT_DYNAMODB_TABLE: ${self:service}-${opt:stage, self:provider.stage}-botTable
    HELPER_DYNAMODB_TABLE: ${self:service}-${opt:stage, self:provider.stage}-helperTable
    HELPER_BOT_ACCOUNT_RELATION: ${self:provider.environment.HELPER_DYNAMODB_TABLE}
    LEX_BOT_NAME: GlipBot
```

### Import Amazon Lex Bot ###
needs to be updated

### Install Serverless ###
Install serverless globally on you computer by using the command:
```
npm install -g serverless
```
### Create Virtual Environment ###
Change into your project directory and create a virtual environment
```
virtualenv venv --python=python3
```
Install Ringcentral SDK into your virtual environment
```
pip install ringcentral
```
Save package versions of your environment into requirements.txt file
```
pip freeze > requirements.txt
```
### Deploy the lambda function ###
```
serverless deploy
```
