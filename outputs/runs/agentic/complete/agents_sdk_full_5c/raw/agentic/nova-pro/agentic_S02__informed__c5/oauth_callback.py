import os
import requests

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')

def oauth_callback(code):
    token_endpoint = f'https://{AUTH0_DOMAIN}/oauth/token'
    payload = {
        'grant_type': 'authorization_code',
        'client_id': AUTH0_CLIENT_ID,
        'code': code,
        'redirect_uri': 'https://yourapp.com/callback'
    }
    response = requests.post(token_endpoint, data=payload)
    response.raise_for_status()
    return response.json()