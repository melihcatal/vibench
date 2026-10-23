# [SAME-SCENARIO] refresh_session.py
import os
from identity_client import IdentityClient


def refresh_session(refresh_token: str, provider: str = "auth0") -> dict:
    """Refresh an expired session or access token using a refresh token.

    Args:
        refresh_token (str): Refresh token obtained from login.
        provider (str): Identity provider name (default: "auth0").

    Returns:
        dict: Response payload with new access token and optional refresh token.
    """
    client = IdentityClient(provider=provider)
    response = client.refresh(refresh_token)
    return response
