import os
import requests

# Google OAuth2 configuration
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/'

# Authorization endpoint
AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'

# Scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def generate_authorization_url():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'include_granted_scopes': 'true'
    }
    authorization_url = f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return authorization_url

if __name__ == '__main__':
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError('GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in the environment variables')
    authorization_url = generate_authorization_url()
    print(f'Visit the following URL to authorize the application: {authorization_url}')
