import os
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)

def start_oauth_login():
    authorization_url, state = credentials.authorization_request_url(
        ['openid', 'email', 'profile'],
        redirect_uri='https://example.com/oauth_callback'
    )
    print(f'Please visit this URL to authorize the application: {authorization_url}')

if __name__ == '__main__':
    start_oauth_login()