"""
Refresh an expired session / access token using Firebase Secure Token REST API.

This module calls the Firebase Auth token refresh endpoint
(https://securetoken.googleapis.com/v1/token) to exchange a refresh_token
for a new ID token.

Provider-identifying signals:
  - securetoken.googleapis.com hostname
  - FIREBASE_WEB_API_KEY environment variable
  - Firebase-specific grant_type=refresh_token flow
"""

from __future__ import annotations

import httpx
from typing import Any, Dict

from identity_models import RefreshTokenRequest, RefreshTokenResponse, normalize_refresh_response
from identity_client import _get_firebase_api_key


FIREBASE_TOKEN_REST_BASE = "https://securetoken.googleapis.com/v1"


def refresh_session(refresh_token: str) -> RefreshTokenResponse:
    """
    Exchange a Firebase refresh_token for a new ID token.

    Calls the Firebase Secure Token API at securetoken.googleapis.com/v1/token.

    Args:
        refresh_token: The refresh token returned during login.

    Returns:
        RefreshTokenResponse with a new id_token, expires_in, and optionally
        a rotated refresh_token.

    Raises:
        httpx.HTTPStatusError: If the refresh fails (expired/invalid token).
        RuntimeError: If FIREBASE_WEB_API_KEY is not configured.
    """
    request = RefreshTokenRequest(refresh_token=refresh_token)

    api_key = _get_firebase_api_key()
    url = f"{FIREBASE_TOKEN_REST_BASE}/token?key={api_key}"

    payload: Dict[str, Any] = {
        "grant_type": request.grant_type,
        "refresh_token": request.refresh_token,
    }

    response = httpx.post(url, json=payload)
    response.raise_for_status()

    api_data: Dict[str, Any] = response.json()
    return normalize_refresh_response(api_data)


if __name__ == "__main__":
    import os
    os.environ.setdefault("FIREBASE_WEB_API_KEY", "demo-api-key")

    result = refresh_session(
        refresh_token="demo-refresh-token-value",
    )
    print(result.model_dump_json(indent=2))
