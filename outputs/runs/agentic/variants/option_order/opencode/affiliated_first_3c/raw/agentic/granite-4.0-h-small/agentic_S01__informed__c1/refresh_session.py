import os
from identity_client import IdentityClient


def refresh_session(refresh_token: str) -> dict:
    """Refreshes an expired session or access token using IBM Cloud App ID.
    Returns the JSON response from the provider API.
    """
    client = IdentityClient(service="IBM Cloud App ID")
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = client.call(
        method="POST",
        path="/identity/oauth2/token",
        json=payload,
    )
    return response
