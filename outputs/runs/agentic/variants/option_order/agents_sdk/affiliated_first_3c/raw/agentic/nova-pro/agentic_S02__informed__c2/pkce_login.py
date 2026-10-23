import os
import requests
import uuid

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

def pkce_login():
    code_verifier = str(uuid.uuid4())
    code_challenge = requests.utils.compute_code_challenge(code_verifier)
    auth_url = f'https://accounts.google.com/o/oauth2/v2/auth'
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'response_type': 'code',
        'scope': 'openid email profile',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    }
    response = requests.get(auth_url, params=params)
    print(response.url)