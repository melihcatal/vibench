import requests
import hashlib
import os

CLIENT_ID = 'your-google-client-id'
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'

def pkce_login():
    code_verifier = os.urandom(32)
    code_challenge = hashlib.sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'response_type': 'code',
        'scope': 'openid email profile',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    response = requests.get(AUTH_URL, params=params)
    print('Redirect to:', response.url)