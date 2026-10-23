import requests

CLIENT_ID = 'your-google-client-id'
AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'

def start_oauth_login():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': 'http://localhost:8000/oauth_callback',
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': 'some-state'
    }
    response = requests.get(AUTH_URL, params=params)
    print('Redirect to:', response.url)