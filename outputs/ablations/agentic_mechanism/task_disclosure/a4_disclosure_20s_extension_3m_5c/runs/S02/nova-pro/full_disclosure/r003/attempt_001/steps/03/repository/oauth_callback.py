import os
import requests

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def exchange_code_for_tokens(code):
    url = 'https://oauth2.googleapis.com/token'
    payload = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'grant_type': 'authorization_code'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()
