import os
import requests

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'
AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'

def start_oauth_login(scopes):
    state = 'xyz'
    params = {
        'client_id': CLIENT_ID,
       'redirect_uri': REDIRECT_URI,
       'response_type': 'code',
       'scope':''.join(scopes),
       'state': state,
        'access_type': 'offline'
    }
    response = requests.get(AUTH_ENDPOINT, params=params)
    return response.url