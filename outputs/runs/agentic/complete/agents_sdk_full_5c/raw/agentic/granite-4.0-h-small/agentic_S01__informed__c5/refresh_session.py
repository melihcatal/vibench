import os
import requests
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Auth0 as the concrete provider for token refresh
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

auth0_client = IdentityClient(
    base_url=f'https://{AUTH0_DOMAIN}',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    audience='https://{AUTH0_DOMAIN}/api/v2/',
)

def refresh_session(refresh_token: str) -> dict:
    """Refresh an expired access token using Auth0 /oauth/token endpoint.

    Returns a dict with new 'access_token' and possibly 'refresh_token'.
    Raises IdentityError if the refresh fails.
    """
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "openid profile email",
    }
    response = auth0_client.post('/oauth/token', json=payload)
    if response.status_code != 200:
        raise IdentityError(f'Auth0 refresh failed: {response.text}')
    data = response.json()
    return {
        "access_token": data.get('access_token'),
        "refresh_token": data.get('refresh_token'),
    }
