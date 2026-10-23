import os
from identity_client import IdentityClient


def email_password_login(email: str, password: str) -> dict:
    """Signs in a user with email and password, returning tokens from IBM Cloud App ID.
    Returns the JSON response from the provider API.
    """
    client = IdentityClient(service="IBM Cloud App ID")
    payload = {"grant_type": "password", "username": email, "password": password}
    response = client.call(
        method="POST",
        path="/identity/oauth2/token",
        json=payload,
    )
    return response
