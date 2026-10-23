import requests
from identity_client import get_client

def oauth_callback(code):
    client = get_client()
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': client.client_id,
        'client_secret': client.client_secret,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    tokens = response.json()
    print('Tokens:', tokens)