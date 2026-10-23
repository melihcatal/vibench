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


def email_password_login(email: str, password: str):
    """Signs in a user with email and password and returns tokens.

    Returns a dict containing access_token and id_token on success,
    raises an exception on failure.
    """
    payload = {
        "username": email,
        "password": password,
        "connection": "Username-Password-Authentication",
        "grant_type": "password",
        "scope": "openid profile email",
    }
    # Use /oauth/token endpoint
    token_response = auth.oauth.login(payload)
    return token_response
