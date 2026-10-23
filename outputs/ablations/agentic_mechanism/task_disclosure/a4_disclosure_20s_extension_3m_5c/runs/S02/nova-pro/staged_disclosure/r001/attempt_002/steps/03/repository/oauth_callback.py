import os
import requests

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

def exchange_code_for_tokens(code):
    """Exchanges an authorization code for tokens using Google OAuth2."""
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    return response.json()
