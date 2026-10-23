import requests

CLIENT_ID = 'YOUR_GOOGLE_CLIENT_ID'
AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth'
REDIRECT_URI = 'http://localhost:8000/oauth2callback'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def start_oauth_login():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'include_granted_scopes': 'true'
    }
    auth_url = f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    print(f'Visit the following URL to start the OAuth login: {auth_url}')

if __name__ == '__main__':
    start_oauth_login()