import os
import boto3

cognito_client_id = os.getenv('COGNITO_CLIENT_ID')
cognito_domain = os.getenv('COGNITO_DOMAIN')

def get_cognito_client():
    return boto3.client('cognito-idp')

def get_authorize_url():
    return f'https://{cognito_domain}/login?response_type=code&client_id={cognito_client_id}&redirect_uri=http://localhost:8000/oauth_callback'