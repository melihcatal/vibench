# identity_client.py

import os
from typing import Any

# External provider import - example using Auth0 Management API
from auth0.v3.management import Client as Auth0Client

# Local configuration (could be loaded from env, .env, or config file)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# Initialize Auth0 Management API client
auth0 = Auth0Client(domain=AUTH0_DOMAIN, token=AUTH0_CLIENT_SECRET)


def create_user(
    email: str, password: str, connection: str = "Username-Password-Authentication"
) -> Any:
    """Create a new email/password user account via Auth0.

    Returns the Auth0 Management API response.
    """
    return auth0.users.create(
        {
            "email": email,
            "password": password,
            "connection": connection,
            "email_verified": False,
        }
    )


def get_user(user_id: str) -> Any:
    """Retrieve user details by user_id."""
    return auth0.users.get(user_id=user_id)


# Add more helper functions as needed for token exchange, password reset, etc.
