# [SAME-SCENARIO] email_password_login.py
import os
from identity_client import IdentityClient


def email_password_login(email: str, password: str, provider: str = "auth0") -> dict:
    """Sign in a user with email and password and return access/refresh tokens.

    Args:
        email (str): User's email address.
        password (str): User's password.
        provider (str): Identity provider name (default: "auth0").

    Returns:
        dict: Response payload containing access and refresh tokens.
    """
    client = IdentityClient(provider=provider)
    payload = {"email": email, "password": password}
    response = client.login(payload)
    return response
