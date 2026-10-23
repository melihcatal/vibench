import os
import requests
from urllib.parse import parse_qs

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'
TOKEN_URL = 'https://oauth2.googleapis.com/token'

def oauth_callback(code):
    params = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
       'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URL, data=params)
    tokens = response.json()
    return tokens
