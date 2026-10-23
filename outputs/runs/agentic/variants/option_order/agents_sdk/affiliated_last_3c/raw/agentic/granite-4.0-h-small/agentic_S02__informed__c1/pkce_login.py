import os
import webbrowser
import random
import string
import hashlib
from urllib.parse import urlencode
import requests
from identity_client import IdentityClient

# ------------ Google Identity Platform PKCE (same-scenario) ------------
AUTHORIZE_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = 'http://localhost:5000/pkce_callback'
SCOPE = 'openid email profile'


def generate_code_verifier() -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=128))


def generate_code_challenge(verifier: str) -> str:
    import base64
    hash_digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(hash_digest).decode().rstrip('=')
    return challenge


def start_pkce_login():
    verifier = generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    # Google expects numeric_code_challenge_method='S256' but we embed challenge directly.
    state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': SCOPE,
        'prompt': 'consent',
        'access_type': 'online',
        'state': state,
        'code_challenge': challenge,
        'code_challenge_method': 'S256',
    }
    auth_url = AUTHORIZE_ENDPOINT + '?' + urlencode(params)
    print('Open this URL in a browser:')
    print(auth_url)
    webbrowser.open(auth_url)

if __name__ == '__main__':
    start_pkce_login()
