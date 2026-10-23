import os
import boto3

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def pkce_login(code_verifier, code_challenge):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={
            'USERNAME': code_verifier,
            'PASSWORD': code_challenge
        },
        ClientId=COGNITO_CLIENT_ID
    )
    print(response)