import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up the OAuth 2.0 credentials
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def get_identity_client():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    return flow

if __name__ == '__main__':
    identity_client = get_identity_client()