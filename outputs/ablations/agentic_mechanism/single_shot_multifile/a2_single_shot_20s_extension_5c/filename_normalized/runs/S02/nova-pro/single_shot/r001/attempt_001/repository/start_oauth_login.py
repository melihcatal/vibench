import os
import requests

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'

def start_oauth_login():
    scope = 'openid email profile'
    params = {
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
       'response_type': 'code',
       'scope': scope,
        'access_type': 'offline',
        'include_granted_scopes': 'true'
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    print(f'Redirect to: {auth_url}')
    return auth_url
