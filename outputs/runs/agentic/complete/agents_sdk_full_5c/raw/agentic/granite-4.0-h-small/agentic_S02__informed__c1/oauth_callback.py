import msal
import os
from requests import Response
from identity_models import AuthCodeResponse, TokenSet
from identity_client import FederatedIdentityClient

# Microsoft Entra ID (Azure AD) configuration
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
TENANT_ID = os.getenv('AZURE_TENANT_ID')
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
REDIRECT_URI = 'http://localhost:5000/oauth_callback'

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)

def exchange_code_for_tokens(auth_code: str) -> TokenSet:
    '''Exchange an authorization code for access and refresh tokens.'''
    # In a real app the callback endpoint receives the auth_code via query string
    token_response: Response = app.acquire_token_by_authorization_code(
        auth_code,
        scopes=['openid', 'profile', 'email'],
        redirect_uri=REDIRECT_URI,
    )
    # Convert raw response to our local model
    return AuthCodeResponse(**token_response).to_token_set()


def oauth_callback(request: dict) -> dict:
    '''Callback handler for the identity provider's redirect.
    Expects `request` dict containing an 'code' field with the auth code.'''
    if 'code' not in request:
        raise ValueError('No authorization code provided')
    code = request['code']
    client = FederatedIdentityClient()
    token_set = client.exchange_code_for_tokens(code)
    # TokenSet contains access_token, id_token, refresh_token, expiration timestamps
    return token_set.as_dict()

if __name__ == '__main__':
    # Simple CLI test
    code = input('Enter auth code: ')
    tokens = exchange_code_for_tokens(code)
    print('Obtained tokens:', tokens)
