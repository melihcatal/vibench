import os
import boto3

cognito_client_id = os.getenv('COGNITO_CLIENT_ID')
cognito_client_secret = os.getenv('COGNITO_CLIENT_SECRET')
cognito_domain = os.getenv('COGNITO_DOMAIN')

def handle_callback(code):
    client = boto3.client('cognito-idp')
    response = client.initiate_auth(
        AuthFlow='CUSTOM_AUTH',
        AuthParameters={'USERNAME': cognito_client_id, 'PASSWORD': cognito_client_secret, 'CODE': code},
        ClientId=cognito_client_id
    )
    print(response)

if __name__ == '__main__':
    handle_callback('authorization_code')