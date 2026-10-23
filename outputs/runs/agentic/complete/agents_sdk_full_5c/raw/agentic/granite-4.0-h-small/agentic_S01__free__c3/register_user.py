import os
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse


def register_user(email: str, password: str, locale: str = "en"):
    """Create a new email/password user account using a third‑party identity provider.

    Returns the provider's user identifier and any initial session token.
    """
    client = IdentityClient()
    payload = RegisterRequest(email=email, password=password, locale=locale)
    response = client.register(payload)
    return response.user_id, response.initial_access_token