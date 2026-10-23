import os
import requests
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

# Configuration
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
TOKEN_URI = 'https://oauth2.googleapis.com/token'

def handle_oauth_callback(authorization_code):
    """Handles the OAuth callback and exchanges an authorization code for tokens."""
    token_response = requests.post(
        TOKEN_URI,
        data={
            'code': authorization_code,
            'client_id': CLIENT_ID,
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
            'redirect_uri': os.getenv('GOOGLE_REDIRECT_URI'),
            'grant_type': 'authorization_code'
        }
    )
    token_response.raise_for_status()
    tokens = token_response.json()
    id_info = id_token.verify_oauth2_token(
        tokens['id_token'],
        google_requests.Request(),
        CLIENT_ID
    )
    return tokens, id_info
