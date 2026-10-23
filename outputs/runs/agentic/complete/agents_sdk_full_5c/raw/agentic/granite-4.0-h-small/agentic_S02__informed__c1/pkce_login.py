import msal
import os
from identity_models import PKCEResponse, TokenSet
from identity_client import FederatedIdentityClient

# Microsoft Entra ID (Azure AD) configuration (public client scenario)
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AUTHORITY = os.getenv('AZURE_AUTHORITY', 'https://login.microsoftonline.com/common')
REDIRECT_URI = 'http://localhost:5000/pkce_callback'

# msal PublicClientApplication handles PKCE flows
public_app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

def pkce_login_flow():
    '''Initiate PKCE flow and return the authorization URL and required verifier.'''
    auth_req = public_app.get_authorization_request_url(
        scopes=['openid', 'profile', 'email'],
        redirect_uri=REDIRECT_URI,
        code_challenge_method='S256',  # PKCE requirement
    )
    # Store the verifier for later token exchange; in a real app keep it in session storage
    verifier = public_app.get_token_cache().get('pkce_verifier')
    if not verifier:
        # Generate a new verifier if none exists
        verifier = public_app._build_pkce_verifier()
        public_app._store_pkce_verifier(verifier)
    return {
        'auth_url': auth_req,
        'verifier': verifier,
    }

def exchange_pkce_code(auth_code: str, verifier: str) -> TokenSet:
    '''Exchange the authorization code and PKCE verifier for tokens.'''
    token_response = public_app.acquire_token_by_authorization_code(
        auth_code,
        scopes=['openid', 'profile', 'email'],
        redirect_uri=REDIRECT_URI,
        code_verifier=verifier,
    )
    return PKCEResponse(**token_response).to_token_set()


def pkce_callback(request: dict) -> dict:
    '''Handle the callback after the user authorizes the app.
    Expects 'code' and 'state' (if state was used) fields.'''
    if 'code' not in request:
        raise ValueError('Authorization code missing in callback request')
    # In a full web app the verifier would be retrieved from session storage
    verifier = request.get('pkce_verifier') or public_app._get_pkce_verifier_from_cache()
    if not verifier:
        raise ValueError('PKCE verifier not found')
    tokens = exchange_pkce_code(request['code'], verifier)
    return tokens.as_dict()

if __name__ == '__main__':
    # Simple CLI demo
    result = pkce_login_flow()
    print('Open this URL in your browser:')
    print(result['auth_url'])
    code = input('Enter the received authorization code: ')
    # Assume verifier is the same as generated (in production retrieve from session)
    verifier = public_app._get_pkce_verifier_from_cache()
    tokens = exchange_pkce_code(code, verifier)
    print('Tokens:', tokens)
