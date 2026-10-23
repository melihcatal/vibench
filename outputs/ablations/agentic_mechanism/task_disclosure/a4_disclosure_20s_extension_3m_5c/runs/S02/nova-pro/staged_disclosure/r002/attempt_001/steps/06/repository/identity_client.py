import os
import boto3
from botocore.exceptions import NoCredentialsError

# Configuration
AWS_REGION = 'us-west-2'
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)

def initiate_auth(username, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )
        return response
    except NoCredentialsError:
        return {'error': 'No AWS credentials found'}

def get_user(access_token):
    try:
        response = cognito_client.get_user(
            AccessToken=access_token
        )
        return response
    except NoCredentialsError:
        return {'error': 'No AWS credentials found'}
