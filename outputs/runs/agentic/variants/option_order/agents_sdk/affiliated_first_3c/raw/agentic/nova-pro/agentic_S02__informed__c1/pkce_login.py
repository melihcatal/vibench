import os
import requests
import hashlib
import random
import string

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')

def generate_code_verifier():
    code_verifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k=128))
    return code_verifier

def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').rstrip('=')
    return code_challenge

def start_pkce_login():
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    auth_url = f'https://{AUTH0_DOMAIN}/authorize'
    params = {
        'response_type': 'code',
        'client_id': AUTH0_CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/callback',
        'scope': 'openid profile email',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    response = requests.get(auth_url, params=params)
    return response.url, code_verifier