# register_user.py

import os
from typing import Any

from identity_client import create_user
from identity_models import CreateUserRequest, normalize_user_response

# Auth0 credentials (or env vars)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


async def register_user(
    email: str, password: str, connection: str = "Username-Password-Authentication"
) -> Any:
    """Create a new email/password user account via Auth0 Management API.

    Returns a normalized UserResponse containing the created user data.
    """
    request = CreateUserRequest(email=email, password=password, connection=connection)
    response_data = create_user(request.email, request.password, request.connection)
    # Normalize the raw Auth0 response into our internal model
    return normalize_user_response(response_data)
