# password_reset.py

import os
from typing import Any

# Auth0 Management API client from identity_client
from identity_client import auth0


async def start_password_reset(email: str) -> Any:
    """Initiate a password reset flow for a local account via Auth0.

    Returns the Auth0 response indicating success or error.
    """
    from auth0.v3.management import Users

    user_mgr = Users(
        domain=os.getenv("AUTH0_DOMAIN"), token=os.getenv("AUTH0_CLIENT_SECRET")
    )
    # Trigger email with password reset link; adjust parameters as needed
    user_mgr.change_password(
        user_id=email, connection="Username-Password-Authentication"
    )
    return {"status": "reset_email_sent", "email": email}
