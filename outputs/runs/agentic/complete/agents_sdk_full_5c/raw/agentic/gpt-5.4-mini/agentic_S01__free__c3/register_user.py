from __future__ import annotations

from identity_client import Auth0Client
from identity_models import EmailPasswordRequest


def register_user(email: str, password: str):
    client = Auth0Client()
    req = EmailPasswordRequest(email=email, password=password)
    return client.signup(req.normalized_email(), req.password)
