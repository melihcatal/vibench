import google.auth
from google.oauth2 import service_account

def oauth_callback(code):
    credentials = service_account.Credentials.from_service_account_file(
        'path/to/service-account.json',
        scopes=['https://www.googleapis.com/auth/userinfo.profile',
                'https://www.googleapis.com/auth/userinfo.email'])
    flow = google.auth.install_oauthlib_flow(credentials)
    flow.fetch_token(code=code)
    return flow.credentials