import os
import requests
from identity_client import IdentityClient
from identity_models import IdentityError

# Use Auth0 as the concrete provider for password reset flow
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')

auth0_client = IdentityClient(
    base_url=f'https://{AUTH0_DOMAIN}',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    audience='https://{AUTH0_DOMAIN}/api/v2/',
)

def initiate_password_reset(email: str, connection: str = 'Username-Password-Authentication') -> bool:
    """Start a password reset for a user with the provided email.

    Returns True if the request was accepted, False otherwise.
    Raises IdentityError for unexpected errors.
    """
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "email": email,
        "connection": connection,
        "url": 'https://example.com/reset-password?ticket={{TICKET}}',
    }
    response = auth0_client.post('/api/v2/tickets/password-change', json=payload)
    if response.status_code == 201:
        return True
    if response.status_code == 202:
        # Accepted but asynchronous
        return True
    raise IdentityError(f'Auth0 password reset request failed: {response.text}')
