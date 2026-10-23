import os
from identity_client import get_identity_client, normalize_email, ensure_password
from identity_models import RegisterUserRequest, RegisterUserResponse


def register_user(email: str, password: str, display_name: str | None = None) -> dict:
    client = get_identity_client()
    req = RegisterUserRequest(email=normalize_email(email), password=ensure_password(password), display_name=display_name)
    user = client.create_user(req)
    return RegisterUserResponse.from_user(user).to_dict()
