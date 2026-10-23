import os
import boto3

def get_cognito_client():
    return boto3.client('cognito-idp', region_name='us-east-1')

def get_user_pool_id():
    return os.getenv('COGNITO_USER_POOL_ID')

def get_client_id():
    return os.getenv('COGNITO_CLIENT_ID')