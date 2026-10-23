from __future__ import annotations

from identity_client import IdentityClient
from identity_models import LoginRequest, extract_tokens


def email_password_login(email: str, password: str) -> dict:
    client = IdentityClient()
    payload = LoginRequest(email=email, password=password).to_payload()
    data = client.post("accounts:signInWithPassword", json=payload)
    return extract_tokens(data)
