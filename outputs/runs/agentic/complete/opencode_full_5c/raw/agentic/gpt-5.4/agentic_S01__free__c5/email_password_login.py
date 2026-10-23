from __future__ import annotations

from identity_client import firebase_identity_url, post_json
from identity_models import (
    IdentityOperationResult,
    LoginRequest,
    normalize_identity_user,
    normalize_token_set,
)


def email_password_login(request: LoginRequest) -> IdentityOperationResult:
    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }
    response = post_json(firebase_identity_url("accounts:signInWithPassword"), payload)
    return IdentityOperationResult(
        provider="google_firebase_identity_platform",
        ok=True,
        message="login_succeeded",
        user=normalize_identity_user(response),
        tokens=normalize_token_set(response),
        raw=response,
    )
