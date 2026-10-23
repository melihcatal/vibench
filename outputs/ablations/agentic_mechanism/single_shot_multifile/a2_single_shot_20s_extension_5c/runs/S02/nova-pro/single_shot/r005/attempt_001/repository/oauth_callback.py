import requests
import os
import urllib.parse

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
TOKEN_URL = 'https://oauth2.googleapis.com/token'

def exchange_code_for_tokens(code, redirect_uri):
    payload = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
       'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()