from __future__ import annotations

from identity_client import firebase_identity_url, post_json
from identity_models import (
    IdentityOperationResult,
    RegisterUserRequest,
    normalize_identity_user,
)


def register_user(request: RegisterUserRequest) -> IdentityOperationResult:
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }
    response = post_json(firebase_identity_url("accounts:signUp"), payload)
    user = normalize_identity_user(response)
    return IdentityOperationResult(
        provider="google_firebase_identity_platform",
        ok=True,
        message="user_registered",
        user=user,
        raw=response,
    )
