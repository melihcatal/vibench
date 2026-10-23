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


def refresh_session(refresh_token: str) -> dict:
    """Refreshes an expired session or access token via Auth0.

    Returns a dict containing new access_token and id_token on success,
    raises an exception on failure.
    """
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
    }
    token_response = auth.oauth.token(payload)
    return token_response
