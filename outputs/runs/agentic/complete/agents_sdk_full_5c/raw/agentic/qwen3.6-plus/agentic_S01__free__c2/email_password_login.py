"""
Sign in a user with email and password using Firebase Identity Toolkit REST API.

This module calls the Firebase Auth REST endpoint
(https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword)
to authenticate a user and return ID/refresh tokens.

Provider-identifying signals:
  - identitytoolkit.googleapis.com hostname
  - FIREBASE_WEB_API_KEY environment variable
  - Firebase-specific response fields (idToken, localId, refreshToken)
"""

from __future__ import annotations

import httpx
from typing import Any, Dict, Optional

from identity_models import LoginRequest, LoginResponse, normalize_login_response
from identity_client import build_firebase_rest_url


def email_password_login(
    email: str,
    password: str,
    return_secure_token: bool = True,
) -> LoginResponse:
    """
    Authenticate a user with email and password via Firebase Auth REST API.

    Calls the Firebase Identity Toolkit signInWithPassword endpoint.

    Args:
        email: User's email address.
        password: User's password.
        return_secure_token: Whether to return a secure ID token.

    Returns:
        LoginResponse containing id_token, refresh_token, expires_in, and local_id.

    Raises:
        httpx.HTTPStatusError: If Firebase returns a non-200 response.
        RuntimeError: If FIREBASE_WEB_API_KEY is not configured.
    """
    request = LoginRequest(
        email=email,
        password=password,
        return_secure_token=return_secure_token,
    )

    url = build_firebase_rest_url("signInWithPassword")
    payload: Dict[str, Any] = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": request.return_secure_token,
    }

    response = httpx.post(url, json=payload)
    response.raise_for_status()

    api_data: Dict[str, Any] = response.json()
    return normalize_login_response(api_data)


if __name__ == "__main__":
    import os
    os.environ.setdefault("FIREBASE_WEB_API_KEY", "demo-api-key")

    result = email_password_login(
        email="newuser@example.com",
        password="SecureP@ss123",
    )
    print(result.model_dump_json(indent=2))
