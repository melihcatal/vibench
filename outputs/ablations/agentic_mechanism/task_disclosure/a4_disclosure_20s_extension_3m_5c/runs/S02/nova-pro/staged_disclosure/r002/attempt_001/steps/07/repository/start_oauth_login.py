import os
import requests

# Google OAuth2 configuration
CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
CLIENT_SECRET = 'YOUR_GOOGLE_CLIENT_SECRET'
REDIRECT_URI = 'http://localhost:8000/oauth2callback'

# Authorization endpoint
AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'

# Token endpoint
TOKEN_URL = 'https://oauth2.googleapis.com/token'

# Scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def get_auth_url():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
    }
    response = requests.get(AUTH_URL, params=params)
    return response.url

if __name__ == '__main__':
    auth_url = get_auth_url()
    print(f'Please visit this URL to authorize the application: {auth_url}')
