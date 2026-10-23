# [SAME-SCENARIO] register_user.py
import os
from identity_client import IdentityClient


def register_user(email: str, password: str, provider: str = "auth0") -> dict:
    """Create a new email/password user account using an external identity provider.

    Args:
        email (str): User's email address.
        password (str): User's password.
        provider (str): Identity provider name (default: "auth0").

    Returns:
        dict: Response payload containing user identifier and metadata.
    """
    client = IdentityClient(provider=provider)
    payload = {"email": email, "password": password}
    response = client.register(payload)
    return response
