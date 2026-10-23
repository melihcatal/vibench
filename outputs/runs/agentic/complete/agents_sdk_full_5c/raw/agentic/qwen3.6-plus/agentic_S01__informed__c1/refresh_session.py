"""
Refreshes an expired session or access token.

Provider: Firebase Authentication
Provider-identifying signals:
  - firebase_admin SDK import
  - Firebase Identity Toolkit REST endpoint (identitytoolkit.googleapis.com)
  - FIREBASE_API_KEY environment variable
  - Google identity API hostname
"""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from identity_models import (
    RefreshSessionRequest,
    RefreshSessionResponse,
    serialize_response,
)

logger = logging.getLogger(__name__)

FIREBASE_API_KEY_ENV = "FIREBASE_API_KEY"
IDENTITY_TOOLKIT_BASE = "https://identitytoolkit.googleapis.com/v1"


def _get_firebase_api_key() -> str:
    """Retrieve the Firebase Web API key from environment."""
    api_key = os.environ.get(FIREBASE_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"Missing {FIREBASE_API_KEY_ENV}. Required to call "
            "https://identitytoolkit.googleapis.com for Firebase token refresh."
        )
    return api_key


def refresh_session(refresh_token: str) -> RefreshSessionResponse:
    """
    Refresh an expired Firebase ID token using the provided refresh token.

    Calls the Firebase Identity Toolkit REST API endpoint:
    POST https://identitytoolkit.googleapis.com/v1/token

    Args:
        refresh_token: The refresh token issued during login.

    Returns:
        RefreshSessionResponse with new id_token, refresh_token, and expiry.
    """
    request = RefreshSessionRequest(refresh_token=refresh_token)

    api_key = _get_firebase_api_key()
    url = f"{IDENTITY_TOOLKIT_BASE}/token?key={api_key}"

    payload = json.dumps({
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            token_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        logger.error(
            "Firebase Identity Toolkit refresh error %s: %s",
            e.code,
            body,
        )
        raise
    except Exception as e:
        logger.error("Firebase token refresh failed: %s", str(e))
        raise

    logger.info(
        "Firebase Auth: Session refreshed successfully, expires_in=%s",
        token_data.get("expires_in"),
    )

    return RefreshSessionResponse(
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        access_token=token_data.get("access_token"),
        expires_in=token_data.get("expires_in"),
        token_type="Bearer",
        provider="firebase",
    )


def refresh_session_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    response = refresh_session(
        refresh_token=data["refresh_token"],
    )
    return serialize_response(response)
