import os
import requests

COGNITO_DOMAIN = os.getenv('COGNITO_DOMAIN')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_CLIENT_SECRET = os.getenv('COGNITO_CLIENT_SECRET')

def oauth_callback(code):
    token_url = f'{COGNITO_DOMAIN}/oauth2/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'client_id': COGNITO_CLIENT_ID,
        'client_secret': COGNITO_CLIENT_SECRET
    }
    response = requests.post(token_url, data=payload)
    tokens = response.json()
    print(tokens)