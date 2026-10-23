import os
from identity_client import FirebaseIdentityClient
from identity_models import UserLoginRequest, AuthResponse, normalize_auth_response


def email_password_login(email: str, password: str) -> AuthResponse:
    client = FirebaseIdentityClient()
    response = client.sign_in(email, password)
    return normalize_auth_response(response)
