import os
from identity_client import FirebaseIdentityClient
from identity_models import (
    UserRegistrationRequest,
    AuthResponse,
    normalize_auth_response,
)


def register_user(email: str, password: str) -> AuthResponse:
    client = FirebaseIdentityClient()
    response = client.create_user(email, password)
    return normalize_auth_response(response)
