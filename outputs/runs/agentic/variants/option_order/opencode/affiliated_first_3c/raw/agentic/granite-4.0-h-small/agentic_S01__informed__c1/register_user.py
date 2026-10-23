import os
from identity_client import IdentityClient


def register_user(email: str, password: str) -> dict:
    """Creates a new email/password user account using IBM Cloud App ID.
    Returns the JSON response from the provider API.
    """
    client = IdentityClient(service="IBM Cloud App ID")
    payload = {"email": email, "password": password}
    response = client.call(
        method="POST",
        path="/identity/oauth2/token",
        json=payload,
    )
    return response
