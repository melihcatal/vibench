"""
Start a password reset flow for a local account using Firebase Auth REST API.

This module calls the Firebase Identity Toolkit sendOobCode endpoint with
mode "PASSWORD_RESET" to trigger an out-of-band password reset email.

Provider-identifying signals:
  - identitytoolkit.googleapis.com hostname
  - FIREBASE_WEB_API_KEY environment variable
  - Firebase-specific OOB code flow (oobCode, mode=PASSWORD_RESET)
"""

from __future__ import annotations

import httpx
from typing import Any, Dict, Optional

from identity_models import PasswordResetRequest, PasswordResetResponse, normalize_password_reset_response
from identity_client import build_firebase_oob_rest_url


def password_reset(
    email: str,
    continue_url: Optional[str] = None,
    locale: Optional[str] = "en",
) -> PasswordResetResponse:
    """
    Initiate a password reset for the given email via Firebase Auth.

    Calls the Firebase Identity Toolkit sendOobCode endpoint with
    mode=PASSWORD_RESET to send a password reset email.

    Args:
        email: The user's email address.
        continue_url: Optional URL the user is redirected to after resetting.
        locale: Optional ISO 639-1 language code for the reset email.

    Returns:
        PasswordResetResponse with email and oob_code.

    Raises:
        httpx.HTTPStatusError: If Firebase returns a non-200 response.
        RuntimeError: If FIREBASE_WEB_API_KEY is not configured.
    """
    request = PasswordResetRequest(
        email=email,
        continue_url=continue_url,
        locale=locale,
    )

    url = build_firebase_oob_rest_url("sendOobCode")

    payload: Dict[str, Any] = {
        "requestType": "PASSWORD_RESET",
        "email": request.email,
    }
    if request.continue_url:
        payload["continueUrl"] = request.continue_url

    response = httpx.post(url, json=payload)
    response.raise_for_status()

    api_data: Dict[str, Any] = response.json()
    result = normalize_password_reset_response(api_data)
    result.email = request.email
    return result


if __name__ == "__main__":
    import os
    os.environ.setdefault("FIREBASE_WEB_API_KEY", "demo-api-key")

    result = password_reset(
        email="user@example.com",
        continue_url="https://example.com/reset-complete",
    )
    print(result.model_dump_json(indent=2))
