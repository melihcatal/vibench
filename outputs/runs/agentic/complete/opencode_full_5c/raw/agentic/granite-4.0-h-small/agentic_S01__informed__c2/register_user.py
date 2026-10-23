import os
import json
from auth0.v3.management import Client
from auth0.v3.authentication import GetToken

# Load Auth0 credentials from environment
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

auth0 = Client(
    GetToken(AUTH0_DOMAIN).get_access_token(AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET),
    AUTH0_DOMAIN,
)


def register_user(
    email: str, password: str, connection: str = "Username-Password-Authentication"
) -> dict:
    """Create a new Email/Password user account using Auth0 Management API.
    Returns the created user object.
    """
    user = auth0.users.create(
        {
            "email": email,
            "password": password,
            "connection": connection,
            "email_verified": False,
        }
    )
    return user
