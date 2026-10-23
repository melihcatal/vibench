import os
import requests

GOOGLE_OAUTH_TOKEN_URL = 'https://oauth2.googleapis.com/token'

def handle_oauth_callback(authorization_code):
    token_data = {
        'code': authorization_code,
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI'),
        'grant_type': 'authorization_code'
    }
    response = requests.post(GOOGLE_OAUTH_TOKEN_URL, data=token_data)
    response.raise_for_status()
    return response.json()
