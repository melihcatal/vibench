import os
import google.auth
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

# Load the client secrets from the environment variable
CLIENT_SECRETS_FILE = os.getenv('GOOGLE_CLIENT_SECRETS_FILE')

def start_oauth_login():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    print('Authentication successful!')

if __name__ == '__main__':
    start_oauth_login()