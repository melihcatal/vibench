import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up the OAuth 2.0 credentials
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def start_oauth_login():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    auth_url, _ = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    print(f'Please go to the following URL to authorize: {auth_url}')

if __name__ == '__main__':
    start_oauth_login()