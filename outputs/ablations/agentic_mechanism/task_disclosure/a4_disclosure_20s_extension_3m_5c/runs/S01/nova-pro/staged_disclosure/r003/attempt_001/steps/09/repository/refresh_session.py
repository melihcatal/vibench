import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Replace with your client_secrets.json file path
CLIENT_SECRETS_FILE = 'client_secrets.json'

# Replace with your scopes
SCOPES = ['https://www.googleapis.com/auth/userinfo.profile']

def refresh_session():
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            with open('token.json', 'w') as token:
                token.write(credentials.to_json())
            return credentials
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
        return credentials

if __name__ == '__main__':
    refresh_session()