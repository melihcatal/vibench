import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up the OAuth 2.0 credentials
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def pkce_login():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.run_local_server(port=0)
    credentials = flow.credentials
    print(f'Access token: {credentials.token}')
    print(f'Refresh token: {credentials.refresh_token}')

if __name__ == '__main__':
    pkce_login()