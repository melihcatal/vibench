# [SAME-SCENARIO] password_reset.py
import os
from identity_client import IdentityClient


def password_reset(email: str, provider: str = "auth0") -> dict:
    """Start a password reset flow for a local user account.

    Args:
        email (str): Email address of the user requesting reset.
        provider (str): Identity provider name (default: "auth0").

    Returns:
        dict: Response payload containing reset token or status.
    """
    client = IdentityClient(provider=provider)
    response = client.forgot_password({"email": email})
    return response
