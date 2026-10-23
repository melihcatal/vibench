import os
import requests

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def oauth_callback(code):
    token_url = 'https://oauth2.googleapis.com/token'
    payload = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'grant_type': 'authorization_code',
    }
    response = requests.post(token_url, data=payload)
    tokens = response.json()
    print(tokens)