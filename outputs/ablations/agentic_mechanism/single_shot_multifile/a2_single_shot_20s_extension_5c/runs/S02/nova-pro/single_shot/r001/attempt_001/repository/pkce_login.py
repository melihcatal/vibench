import os
import requests
import uuid
from urllib.parse import parse_qs

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'

def pkce_login():
    code_verifier = str(uuid.uuid4())
    code_challenge = str(uuid.uuid4())  # Simplified for example
    scope = 'openid email profile'
    params = {
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': scope,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print(f'Redirect to: {auth_url}')
    return auth_url, code_verifier

def exchange_code_for_tokens(code, code_verifier):
    params = {
        'code': code,
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }
    response = requests.post(TOKEN_URL, data=params)
    tokens = response.json()
    return tokens
