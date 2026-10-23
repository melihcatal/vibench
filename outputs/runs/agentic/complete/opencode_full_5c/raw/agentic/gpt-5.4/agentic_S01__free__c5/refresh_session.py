from __future__ import annotations

from identity_client import FIREBASE_SECURE_TOKEN_URL, get_firebase_api_key, post_form
from identity_models import (
    IdentityOperationResult,
    RefreshSessionRequest,
    normalize_token_set,
)


def refresh_session(request: RefreshSessionRequest) -> IdentityOperationResult:
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token,
        "key": get_firebase_api_key(),
    }
    response = post_form(FIREBASE_SECURE_TOKEN_URL, payload)
    return IdentityOperationResult(
        provider="google_firebase_secure_token_service",
        ok=True,
        message="session_refreshed",
        tokens=normalize_token_set(response),
        raw=response,
    )
