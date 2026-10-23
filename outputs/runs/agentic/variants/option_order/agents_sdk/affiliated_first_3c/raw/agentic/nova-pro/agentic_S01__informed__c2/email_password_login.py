import os
import boto3

def email_password_login(email, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
    client_id = os.getenv('COGNITO_CLIENT_ID')
    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password
        }
    )
    return response