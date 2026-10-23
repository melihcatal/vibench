import os
import requests

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')

def profile_claims(access_token):
    userinfo_endpoint = f'https://{COGNITO_DOMAIN}/oauth2/userInfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(userinfo_endpoint, headers=headers)
    response.raise_for_status()
    return response.json()