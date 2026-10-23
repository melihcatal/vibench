import os
import boto3

cognito_client_id = os.getenv('COGNITO_CLIENT_ID')
cognito_domain = os.getenv('COGNITO_DOMAIN')

def fetch_profile(access_token):
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=access_token
    )
    print(response)

if __name__ == '__main__':
    fetch_profile('access_token')