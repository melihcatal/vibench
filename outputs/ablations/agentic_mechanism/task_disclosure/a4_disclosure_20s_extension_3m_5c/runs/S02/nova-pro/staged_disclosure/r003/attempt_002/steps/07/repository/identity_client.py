import os
import boto3

# AWS Cognito configuration
AWS_REGION = os.getenv('AWS_REGION')
USER_POOL_ID = os.getenv('USER_POOL_ID')
CLIENT_ID = os.getenv('CLIENT_ID')

# Initialize the Cognito client
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)

def initiate_auth(username, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthParameters={'USERNAME': username, 'PASSWORD': password},
            AuthFlow='USER_PASSWORD_AUTH'
        )
        return response
    except Exception as e:
        print(f'Error during authentication: {e}')
        return None

def get_token(response):
    if response and 'AuthenticationResult' in response:
        return response['AuthenticationResult']['IdToken']
    return None