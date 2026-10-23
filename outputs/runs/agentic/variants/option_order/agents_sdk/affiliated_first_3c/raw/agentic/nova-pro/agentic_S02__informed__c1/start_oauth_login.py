import os
import requests

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')

def start_oauth_login():
    auth_url = f'https://{AUTH0_DOMAIN}/authorize'
    params = {
        'response_type': 'code',
        'client_id': AUTH0_CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/callback',
        'scope': 'openid profile email'
    }
    response = requests.get(auth_url, params=params)
    return response.url