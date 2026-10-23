import os
import boto3

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')

def oauth_callback(code):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={
            'USERNAME': code,
            'PASSWORD': COGNITO_CLIENT_SECRET
        },
        ClientId=COGNITO_CLIENT_ID
    )
    print(response)