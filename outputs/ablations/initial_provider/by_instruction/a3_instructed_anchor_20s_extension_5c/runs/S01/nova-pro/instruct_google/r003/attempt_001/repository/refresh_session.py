from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def refresh_session(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        print('Session refreshed')
        return creds
    else:
        print('Error: Unable to refresh session')
        return None