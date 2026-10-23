import os
import boto3

def password_reset(email):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
    client_id = os.getenv('COGNITO_CLIENT_ID')
    response = client.forgot_password(
        ClientId=client_id,
        Username=email
    )
    return response