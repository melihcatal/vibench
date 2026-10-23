import os
import boto3
from botocore.exceptions import ClientError

# Configuration
AWS_REGION = 'us-west-2'
USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)


def create_user(email, password):
    try:
        response = cognito_client.sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
        )
        return response
    except ClientError as e:
        print(e)
        return None


def confirm_user(email, confirmation_code):
    try:
        response = cognito_client.confirm_sign_up(
            ClientId=CLIENT_ID,
            Username=email,
            ConfirmationCode=confirmation_code
        )
        return response
    except ClientError as e:
        print(e)
        return None


def authenticate_user(email, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password
            }
        )
        return response
    except ClientError as e:
        print(e)
        return None
