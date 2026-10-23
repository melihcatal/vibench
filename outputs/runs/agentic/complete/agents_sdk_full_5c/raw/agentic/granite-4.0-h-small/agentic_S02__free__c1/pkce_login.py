import os
import random
import string
import requests
from identity_client import IdentityClient
from identity_models import PKCELoginResponse

def pkce_login(redirect_uri):
    client = IdentityClient.from_env()
    # Pick Microsoft Azure AD B2C as the OAuth provider with PKCE
    AUTHORITY_URL = f'https://login.microsoftonline.com/{client.config['TENANT_ID']}/oauth2/v2.0'
    CLIENT_ID = client.config['CLIENT_ID']
    # Generate PKCE parameters
    code_verifier = ''.join(random.choices(string.ascii_letters + string.digits, k=128))
    import hashlib
    import base64
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).rstrip(b'=').decode()
    auth_url = (
        f'{AUTHORITY_URL}/authorize?\n'
        f'response_type=code&\n'
        f'client_id={CLIENT_ID}&\n'
        f'redirect_uri={redirect_uri}&\n'
        f'scope=openid profile email&\n'
        f'code_challenge={code_challenge}&\n'
        f'code_challenge_method=S256&\n'
        f'response_mode=query'
    )
    print('Redirect to PKCE auth URL:', auth_url)
    # The web framework would redirect the user agent here
    # After callback, exchange code for tokens using the verifier
    # Placeholder for token exchange (handled similarly to oauth_callback)
    return PKCELoginResponse(code_verifier=code_verifier)

if __name__ == '__main__':
    pkce_login('http://localhost:5000/callback')
