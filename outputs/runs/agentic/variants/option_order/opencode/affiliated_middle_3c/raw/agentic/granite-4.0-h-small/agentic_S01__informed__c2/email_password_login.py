# email_password_login.py

import os
from typing import Any

from identity_client import create_user
from identity_models import CreateUserRequest, normalize_auth_response

# Auth0 credentials
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


async def email_password_login(email: str, password: str) -> Any:
    """Sign in a user with email and password via Auth0's /oauth/token endpoint.

    Returns a normalized AuthResponse with access/refresh tokens.
    """
    # Auth0 Management API client not needed for login, using direct token endpoint
    from auth0.v3.authentication import Authentication

    auth = Authentication(domain=AUTH0_DOMAIN, client_id=AUTH0_CLIENT_ID)
    result = auth.ro(
        username=email,
        password=password,
        client_id=AUTH0_CLIENT_ID,
        realm="Username-Password-Authentication",
    )
    return normalize_auth_response(result)
