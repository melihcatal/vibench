import os
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secret.json'

def pkce_login():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'])
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')
    print('Please go to this URL and authorize: ', authorization_url)