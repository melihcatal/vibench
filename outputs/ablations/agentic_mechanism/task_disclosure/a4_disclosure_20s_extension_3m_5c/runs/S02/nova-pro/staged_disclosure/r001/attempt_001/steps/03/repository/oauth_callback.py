import os
import requests

# Google OAuth2 configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI')

def exchange_code_for_tokens(code):
    """Exchanges an authorization code for access and refresh tokens."""
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    response = requests.post(token_url, data=token_data)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    import sys
    if len(sys.argv)!= 2:
        print('Usage: python oauth_callback.py <authorization_code>')
        sys.exit(1)
    authorization_code = sys.argv[1]
    tokens = exchange_code_for_tokens(authorization_code)
    print('Access Token:', tokens['access_token'])
    print('Refresh Token:', tokens['refresh_token'])