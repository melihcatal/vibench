import os
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

def start_oauth_login():
    CLIENT_SECRETS_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials