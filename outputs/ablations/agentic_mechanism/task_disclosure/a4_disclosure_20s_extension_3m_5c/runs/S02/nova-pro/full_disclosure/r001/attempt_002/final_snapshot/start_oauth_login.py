import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the OAuth 2.0 client ID and secret
CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

# Define the OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def start_oauth_login():
    flow = InstalledAppFlow.from_client_config({
        'installed': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'scopes': SCOPES
        }
    }, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

if __name__ == '__main__':
    credentials = start_oauth_login()
    print('OAuth login successful!')