import os
import requests

GOOGLE_OAUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'

def start_oauth_login():
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
    scope = 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email'
    response_type = 'code'
    access_type = 'offline'
    include_granted_scopes = 'true'

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': scope,
        'response_type': response_type,
        'access_type': access_type,
        'include_granted_scopes': include_granted_scopes,
    }

    response = requests.get(GOOGLE_OAUTH_URL, params=params)
    print(response.url)

if __name__ == '__main__':
    start_oauth_login()