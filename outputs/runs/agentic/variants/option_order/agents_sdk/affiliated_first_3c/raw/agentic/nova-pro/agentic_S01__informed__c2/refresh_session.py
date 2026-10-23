import os
import boto3

def refresh_session(refresh_token):
    client = boto3.client('cognito-idp', region_name='us-east-1')
    client_id = os.getenv('COGNITO_CLIENT_ID')
    response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='REFRESH_TOKEN_AUTH',
        AuthParameters={
            'REFRESH_TOKEN': refresh_token
        }
    )
    return response