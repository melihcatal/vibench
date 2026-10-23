import boto3

def get_identity_client():
    return boto3.client('cognito-idp')

def get_identity_config():
    return {
        'client_id': 'YOUR_CLIENT_ID',
        'user_pool_id': 'YOUR_USER_POOL_ID'
    }