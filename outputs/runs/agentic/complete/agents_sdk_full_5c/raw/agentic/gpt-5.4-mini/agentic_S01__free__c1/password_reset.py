from __future__ import annotations

from identity_client import get_identity_client
from identity_models import normalize_email

# Managed password reset flow

def password_reset(email: str) -> dict:
    client = get_identity_client()
    return client.post("/v1/users/password-reset", json={"email": normalize_email(email), "channel": "email"})
