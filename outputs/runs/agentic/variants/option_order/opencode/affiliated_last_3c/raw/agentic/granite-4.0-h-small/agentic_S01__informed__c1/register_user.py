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


def register_user(email: str, password: str) -> dict:
    """Creates a new email/password user account via Auth0.

    Returns the created user object on success, raises an exception on failure.
    """
    payload = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    # Call Auth0 Management API endpoint to create user
    response = auth.users.create(payload)
    return response
