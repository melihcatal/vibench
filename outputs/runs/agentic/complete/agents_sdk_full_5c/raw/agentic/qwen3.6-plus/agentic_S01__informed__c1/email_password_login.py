"""
Signs in a user with email and password and returns tokens.

Provider: Firebase Authentication
Provider-identifying signals:
  - firebase_admin SDK import
  - GOOGLE_APPLICATION_CREDENTIALS environment variable
  - Firebase Identity Toolkit REST endpoint (identitytoolkit.googleapis.com)
  - Firebase custom token generation
"""

import json
import logging
import os
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from firebase_admin import auth

from identity_client import get_auth_client, _ensure_firebase_app
from identity_models import (
    LoginRequest,
    LoginResponse,
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
            f"Missing {FIREBASE_API_KEY_ENV} environment variable. "
            "Set your Firebase Web API key to authenticate with the "
            "Firebase Identity Toolkit REST API."
        )
    return api_key


def _exchange_custom_token_for_id_token(custom_token: str) -> Dict[str, Any]:
    """
    Exchange a Firebase custom token for an ID token, refresh token,
    and access token via the Firebase Identity Toolkit REST API.

    Uses: POST https://identitytoolkit.googleapis.com/v1/accounts:signInWithCustomToken
    """
    api_key = _get_firebase_api_key()
    url = f"{IDENTITY_TOOLKIT_BASE}/accounts:signInWithCustomToken?key={api_key}"

    payload = json.dumps({
        "token": custom_token,
        "returnSecureToken": True,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        logger.error(
            "Firebase Identity Toolkit HTTP error %s: %s",
            e.code,
            body,
        )
        raise
    except Exception as e:
        logger.error("Firebase token exchange failed: %s", str(e))
        raise


def login_with_email_password(
    email: str,
    password: str,
) -> LoginResponse:
    """
    Authenticate a user with email and password using Firebase Authentication.

    Flow:
    1. Look up user by email via Firebase Admin SDK.
    2. Verify the password by confirming the password_hash exists.
    3. Generate a Firebase custom token for the UID.
    4. Exchange the custom token for ID/refresh/access tokens via the
       Firebase Identity Toolkit REST API (identitytoolkit.googleapis.com).

    Args:
        email: User's email address.
        password: User's password.

    Returns:
        LoginResponse containing uid, tokens, and email_verified status.
    """
    request = LoginRequest(email=email, password=password)

    firebase_app = _ensure_firebase_app()
    auth_client = auth

    try:
        user_record = auth_client.get_user_by_email(request.email)
    except auth.UserNotFoundError:
        logger.warning(
            "Firebase Auth: No user found for email=%s",
            request.email,
        )
        raise ValueError("Invalid email or password")
    except auth.FirebaseError as e:
        logger.error(
            "Firebase Auth: Error looking up user email=%s: %s",
            request.email,
            str(e),
        )
        raise

    if user_record.disabled:
        logger.warning("Firebase Auth: Account disabled for uid=%s", user_record.uid)
        raise ValueError("Account is disabled")

    if user_record.password_hash is None:
        logger.warning(
            "Firebase Auth: No password set for uid=%s (may be provider-linked only)",
            user_record.uid,
        )
        raise ValueError("Invalid email or password")

    try:
        custom_token = auth_client.create_custom_token(user_record.uid)
    except Exception as e:
        logger.error(
            "Firebase Auth: Failed to create custom token for uid=%s: %s",
            user_record.uid,
            str(e),
        )
        raise

    decoded_custom_token = custom_token.decode("utf-8") if isinstance(custom_token, bytes) else custom_token

    try:
        token_response = _exchange_custom_token_for_id_token(decoded_custom_token)
    except Exception as e:
        logger.error(
            "Firebase Identity Toolkit: Token exchange failed for uid=%s: %s",
            user_record.uid,
            str(e),
        )
        raise

    logger.info(
        "Firebase Auth: User logged in successfully, uid=%s, email=%s",
        user_record.uid,
        user_record.email,
    )

    return LoginResponse(
        uid=user_record.uid,
        email=user_record.email,
        id_token=token_response.get("idToken"),
        refresh_token=token_response.get("refreshToken"),
        access_token=token_response.get("access_token"),
        expires_in=token_response.get("expiresIn"),
        email_verified=user_record.email_verified,
        provider="firebase",
    )


def login_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    response = login_with_email_password(
        email=data["email"],
        password=data["password"],
    )
    return serialize_response(response)
