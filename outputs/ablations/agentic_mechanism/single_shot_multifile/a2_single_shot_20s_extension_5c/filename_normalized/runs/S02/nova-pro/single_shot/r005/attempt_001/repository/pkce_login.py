import requests
import os
import urllib.parse
import hashlib
import base64

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'

def generate_code_verifier():
    code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8').replace('=', '')
    return code_verifier

def generate_code_challenge(code_verifier):
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').replace('=', '')
    return code_challenge

def start_pkce_login(redirect_uri):
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    scopes = 'openid email profile'
    params = {
        'client_id': CLIENT_ID,
       'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': scopes,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    login_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return login_url, code_verifier

def exchange_code_for_tokens(code, redirect_uri, code_verifier):
    payload = {
        'code': code,
        'client_id': CLIENT_ID,
       'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
        'code_verifier': code_verifier
    }
    response = requests.post(TOKEN_URL, data=payload)
    response.raise_for_status()
    return response.json()