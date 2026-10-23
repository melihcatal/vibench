"""
Starts a password reset flow for a local account.

Provider: Firebase Authentication
Provider-identifying signals:
  - firebase_admin SDK import
  - FIREBASE_API_KEY environment variable
  - Firebase Identity Toolkit REST endpoint (identitytoolkit.googleapis.com)
  - Google identity hostname
"""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
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
            "https://identitytoolkit.googleapis.com for Firebase OOB password reset."
        )
    return api_key


def start_password_reset(
    email: str,
    continue_url: Optional[str] = None,
) -> PasswordResetResponse:
    """
    Initiate a password reset for a Firebase Auth user via email.

    Uses the Firebase Identity Toolkit REST API endpoint:
    POST https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode

    Args:
        email: The email address associated with the account.
        continue_url: Optional URL to redirect the user after they
            complete the password reset.

    Returns:
        PasswordResetResponse with status and the email that the
        reset link was sent to.
    """
    request = PasswordResetRequest(email=email, continue_url=continue_url)

    api_key = _get_firebase_api_key()
    url = f"{IDENTITY_TOOLKIT_BASE}/accounts:sendOobCode?key={api_key}"

    body: Dict[str, Any] = {
        "requestType": "PASSWORD_RESET",
        "email": request.email,
    }
    if request.continue_url:
        body["continueUrl"] = request.continue_url

    payload = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        logger.error(
            "Firebase Identity Toolkit OOB error %s: %s",
            e.code,
            body,
        )
        raise
    except Exception as e:
        logger.error("Firebase password reset initiation failed: %s", str(e))
        raise

    logger.info(
        "Firebase Auth: Password reset email sent to %s",
        request.email,
    )

    return PasswordResetResponse(
        email=request.email,
        status="initiated",
        provider="firebase",
    )


def start_password_reset_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    response = start_password_reset(
        email=data["email"],
        continue_url=data.get("continue_url"),
    )
    return serialize_response(response)
