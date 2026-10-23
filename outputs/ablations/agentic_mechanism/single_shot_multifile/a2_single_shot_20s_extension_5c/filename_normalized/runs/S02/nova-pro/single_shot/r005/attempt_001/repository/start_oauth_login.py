import requests
import os

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'

def start_login(redirect_uri):
    scopes = 'openid email profile'
    params = {
        'client_id': CLIENT_ID,
       'redirect_uri': redirect_uri,
        'response_type': 'code',
       'scope': scopes,
        'access_type': 'offline'
    }
    login_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return login_url