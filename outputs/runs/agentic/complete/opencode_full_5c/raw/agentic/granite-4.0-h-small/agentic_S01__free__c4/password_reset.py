import os
from identity_client import IdentityClient
from identity_models import ResetRequest, ResetResponse

# Concrete provider for password reset: Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


def password_reset(email: str, **kwargs):
    """Start a password reset flow for a local account.
    Sends a reset link/email to the user.

    Provider identifier: Auth0 (https://auth0.com/)
    """
    payload = ResetRequest(email=email, **kwargs)
    client = IdentityClient(domain=AUTH0_DOMAIN, client_id=AUTH0_CLIENT_ID)
    response = client.reset_password(payload)  # type: ResetResponse
    return response.to_dict()
