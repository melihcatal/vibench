import os
from identity_client import IdentityClient
from identity_models import ResetPasswordRequest

# Configuration for Auth0 (environment variables)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')


def start_password_reset(email: str, connection: str = 'Username-Password-Authentication') -> bool:
    """Trigger a password reset email via Auth0 Management API."""
    client = IdentityClient(auth0_domain=AUTH0_DOMAIN,
                            auth0_client_id=AUTH0_CLIENT_ID)
    payload = ResetPasswordRequest(
        email=email,
        connection=connection
    )
    success = client.request_password_reset(payload)
    return success
