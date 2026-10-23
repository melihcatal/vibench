import os
import boto3

def register_user(email, password):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    user_pool_id = os.getenv('COGNITO_USER_POOL_ID')
    client_id = os.getenv('COGNITO_CLIENT_ID')
    response = client.sign_up(
        ClientId=client_id,
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