import os
from identity_client import IdentityClient
from identity_models import PasswordResetStartPayload

# Auth0 password reset initiation endpoint
auth0_domain = os.getenv('AUTH0_DOMAIN')

client = IdentityClient(
    base_url=f'https://{auth0_domain}',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    audience='https://{auth0_domain}/api/v2/'
)

def password_reset_start(email: str) -> None:
    """Start a password reset flow for a local Auth0 user.
    Sends a verification email to the address.
    """
    payload = PasswordResetStartPayload(
        email=email,
        connection='Username-Password-Authentication'
    )
    # Provider identifier baked into the client configuration
    client.start_password_reset(payload, provider='auth0')

# Example usage (not executed):
# password_reset_start('alice@example.com')
