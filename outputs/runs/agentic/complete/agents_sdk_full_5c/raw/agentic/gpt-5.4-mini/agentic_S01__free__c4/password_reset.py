from __future__ import annotations

from identity_client import IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str) -> dict:
    client = IdentityClient()
    payload = PasswordResetRequest(email=email).to_payload()
    return client.post("accounts:sendOobCode", json=payload)
