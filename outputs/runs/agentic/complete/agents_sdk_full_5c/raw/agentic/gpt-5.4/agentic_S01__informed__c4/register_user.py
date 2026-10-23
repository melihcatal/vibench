from __future__ import annotations

from identity_client import FirebaseIdentityClient
from identity_models import RegisterUserRequest, normalize_firebase_user_response


def register_user(email: str, password: str, display_name: str | None = None):
    client = FirebaseIdentityClient()
    request_model = RegisterUserRequest(email=email, password=password, display_name=display_name)
    payload = client.post_identity("accounts:signUp", request_model.to_identity_payload())
    return normalize_firebase_user_response(payload)
