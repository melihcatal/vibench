import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request

def get_credentials():
    return service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY'),
        scopes=['https://www.googleapis.com/auth/identitytoolkit.googleapis.com']
    )

def get_access_token():
    credentials = get_credentials()
    credentials.refresh(Request())
    return credentials.token