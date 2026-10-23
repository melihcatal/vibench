import os
import requests

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def start_oauth_login():
    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'response_type': 'code',
        'scope': 'openid email profile',
    }
    response = requests.get(auth_url, params=params)
    print(response.url)