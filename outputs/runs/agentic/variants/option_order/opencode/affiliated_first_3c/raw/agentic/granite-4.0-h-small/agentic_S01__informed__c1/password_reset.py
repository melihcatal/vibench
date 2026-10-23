import os
from identity_client import IdentityClient


def password_reset(email: str) -> dict:
    """Starts a password reset flow for a local account using IBM Cloud App ID.
    Returns the JSON response from the provider API.
    """
    client = IdentityClient(service="IBM Cloud App ID")
    payload = {"email": email}
    response = client.call(
        method="POST",
        path="/identity/v1/identity/reset_password",
        json=payload,
    )
    return response
