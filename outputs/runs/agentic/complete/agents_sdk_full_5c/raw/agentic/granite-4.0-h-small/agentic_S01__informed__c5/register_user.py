import os
import requests
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Auth0 as the concrete provider for email/password registration
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

auth0_client = IdentityClient(
    base_url=f'https://{AUTH0_DOMAIN}',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    audience='https://{AUTH0_DOMAIN}/api/v2/',
)

def register_user(email: str, password: str, connection: str = 'Username-Password-Authentication') -> dict:
    """Create a new Email/Password user account using Auth0 Management API.

    Returns the created user object.
    Raises IdentityError on failure.
    """
    payload = {
        "email": email,
        "password": password,
        "connection": connection,
        "email_verified": False,
    }
    response = auth0_client.post(
        '/api/v2/users',
        json=payload,
    )
    if response.status_code != 201:
        raise IdentityError(f'Auth0 registration failed: {response.text}')
    return response.json()
