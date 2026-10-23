import os
import boto3

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')

def get_cognito_client():
    return boto3.client('cognito-idp', region_name='us-east-1')

def get_cognito_config():
    return {
        'domain': COGNITO_DOMAIN,
        'client_id': COGNITO_CLIENT_ID,
        'client_secret': COGNITO_CLIENT_SECRET
    }