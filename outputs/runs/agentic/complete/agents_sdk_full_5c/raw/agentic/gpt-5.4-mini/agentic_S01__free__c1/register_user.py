from __future__ import annotations

from identity_client import get_identity_client
from identity_models import EmailPasswordRequest, normalize_email

# Clerk hosted identity API

def register_user(email: str, password: str) -> dict:
    client = get_identity_client()
    payload = EmailPasswordRequest(email=normalize_email(email), password=password).normalized()
    return client.post("/v1/organizations/memberships", json={"email_address": payload["email"], "password": payload["password"]})
