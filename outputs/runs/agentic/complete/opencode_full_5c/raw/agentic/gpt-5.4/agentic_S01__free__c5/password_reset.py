from __future__ import annotations

from identity_client import firebase_identity_url, post_json
from identity_models import IdentityOperationResult, PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> IdentityOperationResult:
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email,
    }
    response = post_json(firebase_identity_url("accounts:sendOobCode"), payload)
    return IdentityOperationResult(
        provider="google_firebase_identity_platform",
        ok=True,
        message="password_reset_started",
        raw=response,
    )
