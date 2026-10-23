import os
import boto3

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def fetch_profile_claims(access_token):
    client = boto3.client('cognito-idp')
    response = client.get_user(
        AccessToken=access_token
    )
    print(response)