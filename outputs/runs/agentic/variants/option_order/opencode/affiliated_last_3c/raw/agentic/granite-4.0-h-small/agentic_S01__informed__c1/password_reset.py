import os
from auth0 import Authentication

# Auth0 configuration loaded from environment variables
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# Initialize Auth0 authentication client
auth = Authentication(
    domain=AUTH0_DOMAIN, client_id=AUTH0_CLIENT_ID, client_secret=AUTH0_CLIENT_SECRET
)


def start_password_reset(email: str) -> bool:
    """Starts a password reset flow for a local account.

    Returns True on success, raises an exception on failure.
    """
    payload = {"email": email, "connection": "Username-Password-Authentication"}
    # Trigger password reset email
    auth.users.reset_password(payload)
    return True
