from __future__ import annotations

from identity_client import Auth0Client
from identity_models import ResetRequest


def password_reset(email: str):
    client = Auth0Client()
    req = ResetRequest(email=email)
    return client.password_change_ticket(req.normalized_email())
