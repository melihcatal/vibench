import os
from identity_client import IdentityClient

def refresh_session(refresh_token: str):
    """Refresh an expired session or access token using the stored refresh_token.
    Returns a new access token (and id_token) on success.
    Raises RuntimeError if the refresh fails.
    """
    client = IdentityClient()
    response = client.refresh_token(refresh_token)
    if response.get('access_token'):
        return response['access_token']
    raise RuntimeError(f"Refresh failed: {response}")
