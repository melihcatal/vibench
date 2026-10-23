import os
import requests
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Auth0 as the concrete provider for email/password login
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

auth0_client = IdentityClient(
    base_url=f'https://{AUTH0_DOMAIN}',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    audience='https://{AUTH0_DOMAIN}/api/v2/',
)

def email_password_login(email: str, password: str, grant_type: str = 'password') -> dict:
    """Exchange email/password for Access and ID Tokens via Auth0 /oauth/token endpoint.

    Returns a dict containing 'access_token' and 'id_token'.
    Raises IdentityError on authentication failure.
    """
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": auth0_client.audience,
        "grant_type": grant_type,
        "username": email,
        "password": password,
        "scope": 'openid profile email',
    }
    response = auth0_client.post('/oauth/token', json=payload)
    if response.status_code != 200:
        raise IdentityError(f'Auth0 login failed: {response.text}')
    data = response.json()
    return {
        "access_token": data.get('access_token'),
        "id_token": data.get('id_token'),
    }
