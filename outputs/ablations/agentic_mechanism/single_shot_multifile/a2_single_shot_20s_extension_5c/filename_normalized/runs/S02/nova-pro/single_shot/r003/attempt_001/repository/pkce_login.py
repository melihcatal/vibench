import os
import requests
import hashlib
import random

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'
AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'

def generate_code_verifier():
    code_verifier = ''.join(random.choices('abcdef0123456789', k=64))
    return code_verifier

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = code_challenge.decode('utf-8', 'ignore')
    return code_challenge

def start_pkce_login(scopes):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state = 'xyz'
    params = {
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
       'scope':''.join(scopes),
       'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    response = requests.get(AUTH_ENDPOINT, params=params)
    return response.url, code_verifier

def exchange_code_for_tokens(code, code_verifier):
    data = {
        'code': code,
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }
    response = requests.post(TOKEN_ENDPOINT, data=data)
    response.raise_for_status()
    return response.json()