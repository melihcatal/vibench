import os
import requests

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'

def oauth_callback(code):
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
       'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_ENDPOINT, data=data)
    response.raise_for_status()
    return response.json()