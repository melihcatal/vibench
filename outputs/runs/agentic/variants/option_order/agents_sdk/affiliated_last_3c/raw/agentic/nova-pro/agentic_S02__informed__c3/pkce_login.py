import os
import secrets
from google_auth_oauthlib.flow import Flow

def pkce_login():
    flow = Flow.from_client_secrets_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS'),
        scopes=['openid', 'email', 'profile']
    )
    flow.redirect_uri = 'https://example.com/oauth_callback'
    code_verifier = secrets.token_urlsafe(96)
    flow.run_local_server(port=0, code_verifier=code_verifier)
    tokens = flow.credentials
    print(tokens)

if __name__ == '__main__':
    pkce_login()