import requests
from identity_client import get_auth0_client

def oauth_callback(code):
    client = get_auth0_client()
    token_url = f'https://{client.domain}/oauth/token'
    data = {
        'grant_type': 'authorization_code',
        'client_id': client.client_id,
        'code': code,
        'redirect_uri': 'https://yourapp.com/callback'
    }
    response = requests.post(token_url, data=data)
    return response.json()