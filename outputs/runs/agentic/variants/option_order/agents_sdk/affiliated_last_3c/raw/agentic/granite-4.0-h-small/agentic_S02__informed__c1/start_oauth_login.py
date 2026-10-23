import os
import webbrowser
import requests
from identity_client import IdentityClient

# ------------ Google Identity Platform OAuth (same-scenario) ------------
AUTHORIZE_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_ENDPOINT = 'https://oauth2.googleapis.com/token'
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = 'http://localhost:5000/oauth_callback'
SCOPE = 'openid email profile'

def start_oauth_login():
    """Redirect user to Google consent screen."""
    state = 'state12345'  # replace with securely generated value
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'response_type': 'code',
        'prompt': 'consent',
        'access_type': 'online',
        'state': state,
        'code_challenge_method': 'S256',
        'code_challenge': generate_pkce_challenge(),
    }
    auth_url = AUTHORIZE_ENDPOINT + "?" + requests.compat.urlencode(params)
    print("Open this URL in a browser:")
    print(auth_url)
    webbrowser.open(auth_url)

def generate_pkce_challenge() -> str:
    import base64, hashlib, secrets
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip('=',)
    return code_challenge

if __name__ == '__main__':
    start_oauth_login()