import os
import json
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error

# Auth0 configuration
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

# PKCE parameters
CODE_VERIFIER = os.getenv('CODE_VERIFIER')
CODE_CHALLENGE = os.getenv('CODE_CHALLENGE')

def initiate_pkce_login():
    try:
        # Initialize the Auth0 client
        auth0 = GetToken(AUTH0_DOMAIN)
        
        # Request authorization code
        authorization_url = auth0.authorize_url(
            client_id=AUTH0_CLIENT_ID,
            response_type='code',
            redirect_uri='https://your-app.com/callback',
            code_challenge=CODE_CHALLENGE,
            code_challenge_method='S256'
        )
        
        print(f'Authorization URL: {authorization_url}')
    except Auth0Error as e:
        print(f'Error initiating PKCE login: {e}')

def exchange_code_for_tokens(authorization_code):
    try:
        # Initialize the Auth0 client
        auth0 = GetToken(AUTH0_DOMAIN)
        
        # Exchange authorization code for tokens
        tokens = auth0.get_oauth_token(
            grant_type='authorization_code',
            client_id=AUTH0_CLIENT_ID,
            client_secret=AUTH0_CLIENT_SECRET,
            code=authorization_code,
            redirect_uri='https://your-app.com/callback',
            code_verifier=CODE_VERIFIER
        )
        
        print(f'Tokens: {json.dumps(tokens, indent=2)}')
    except Auth0Error as e:
        print(f'Error exchanging code for tokens: {e}')

if __name__ == '__main__':
    initiate_pkce_login()