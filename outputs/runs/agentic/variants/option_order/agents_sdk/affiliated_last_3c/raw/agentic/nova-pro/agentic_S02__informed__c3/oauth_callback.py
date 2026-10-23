import os
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file(
    os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
)

def oauth_callback(authorization_response):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        scopes=['openid', 'email', 'profile']
    )
    flow.redirect_uri = 'https://example.com/oauth_callback'
    tokens = flow.fetch_token(authorization_response=authorization_response)
    print(tokens)

if __name__ == '__main__':
    oauth_callback('authorization_response')