import os
import boto3
from botocore.exceptions import ClientError

# Configuration
COGNITO_REGION = os.getenv('COGNITO_REGION')
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_APP_CLIENT_ID = os.getenv('COGNITO_APP_CLIENT_ID')

# Cognito Client
cognito_client = boto3.client('cognito-idp', region_name=COGNITO_REGION)

def initiate_auth(username, password):
    try:
        response = cognito_client.initiate_auth(
            ClientId=COGNITO_APP_CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': username, 'PASSWORD': password}
        )
        return response
    except ClientError as e:
        print(e)
        return None

def confirm_sign_up(username, confirmation_code):
    try:
        response = cognito_client.confirm_sign_up(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code
        )
        return response
    except ClientError as e:
        print(e)
        return None

def resend_confirmation_code(username):
    try:
        response = cognito_client.resend_confirmation_code(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=username
        )
        return response
    except ClientError as e:
        print(e)
        return None

def forgot_password(username):
    try:
        response = cognito_client.forgot_password(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=username
        )
        return response
    except ClientError as e:
        print(e)
        return None

def confirm_forgot_password(username, confirmation_code, new_password):
    try:
        response = cognito_client.confirm_forgot_password(
            ClientId=COGNITO_APP_CLIENT_ID,
            Username=username,
            ConfirmationCode=confirmation_code,
            Password=new_password
        )
        return response
    except ClientError as e:
        print(e)
        return None