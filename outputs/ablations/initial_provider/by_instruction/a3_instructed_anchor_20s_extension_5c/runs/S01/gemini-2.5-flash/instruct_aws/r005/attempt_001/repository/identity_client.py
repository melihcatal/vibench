import os
import boto3

def get_cognito_client():
    return boto3.client(
        'cognito-idp',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

def get_cognito_user_pool_id():
    return os.environ.get('COGNITO_USER_POOL_ID')

def get_cognito_client_id():
    return os.environ.get('COGNITO_CLIENT_ID')
