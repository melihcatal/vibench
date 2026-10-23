from __future__ import annotations

from identity_client import FirebaseIdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str):
    client = FirebaseIdentityClient()
    request_model = PasswordResetRequest(email=email)
    return client.post_identity("accounts:sendOobCode", request_model.to_identity_payload())
