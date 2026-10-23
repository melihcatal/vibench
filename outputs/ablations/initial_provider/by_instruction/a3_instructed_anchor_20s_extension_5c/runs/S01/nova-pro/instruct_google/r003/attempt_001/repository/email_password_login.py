from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']

def email_password_login(email, password):
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', scopes=SCOPES)
    creds = flow.run_local_server(port=0)
    if creds and creds.valid:
        service = build('oauth2', 'v2', credentials=creds)
        user_info = service.userinfo().get().execute()
        print('User ID:', user_info.get('id'))
        return creds
    else:
        print('Error: Unable to login')
        return None