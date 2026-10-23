from __future__ import annotations

from identity_client import FirebaseIdentityClient
from identity_models import LoginRequest, normalize_firebase_auth_response


def email_password_login(email: str, password: str):
    client = FirebaseIdentityClient()
    request_model = LoginRequest(email=email, password=password)
    payload = client.post_identity("accounts:signInWithPassword", request_model.to_identity_payload())
    return normalize_firebase_auth_response(payload)
