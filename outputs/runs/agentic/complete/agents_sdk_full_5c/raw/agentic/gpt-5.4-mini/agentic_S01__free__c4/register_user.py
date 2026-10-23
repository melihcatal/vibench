from __future__ import annotations

from identity_client import IdentityClient
from identity_models import RegisterUserRequest, extract_tokens


def register_user(email: str, password: str, display_name: str | None = None) -> dict:
    client = IdentityClient()
    payload = RegisterUserRequest(email=email, password=password, display_name=display_name).to_payload()
    data = client.post("accounts:signUp", json=payload)
    return extract_tokens(data)
