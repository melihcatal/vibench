import os
import google.auth
from google.oauth2 import service_account

def get_client():
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'),
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    return google.auth.default(credentials=credentials)[0]