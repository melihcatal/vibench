"""
Refresh an expired session or access token using Firebase Authentication.
Provider: Firebase Auth (Google Cloud Identity Toolkit API)
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional, Tuple

from identity_client import FirebaseIdentityClient
from identity_models import TokenRefreshRequest, SessionResponse, AuthError


FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_IDENTITY_TOOLKIT_BASE = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_TOKEN_REFRESH_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/token"


def refresh_session(
    refresh_token: str,
    api_key: Optional[str] = None,
) -> Tuple[Optional[SessionResponse], Optional[AuthError]]:
    """
    Refresh an expired access token using a refresh token via Firebase Auth.

    Args:
        refresh_token: The refresh token from the original login
        api_key: Firebase API key (falls back to FIREBASE_API_KEY env var)

    Returns:
        Tuple of (SessionResponse, AuthError) - one will be None
    """
    key = api_key or FIREBASE_API_KEY
    if not key:
        return None, AuthError(
            code=400,
            message="Firebase API key not configured"
        )

    req = TokenRefreshRequest(refresh_token=refresh_token)

    url = f"{FIREBASE_TOKEN_REFRESH_ENDPOINT}?key={key}"
    payload = req.to_firebase_payload()

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        session = _normalize_refresh_response(data)
        return session, None

    except requests.exceptions.HTTPError as exc:
        try:
            error_data = exc.response.json()
            auth_error = AuthError.from_firebase_error(error_data)
        except (json.JSONDecodeError, KeyError):
            auth_error = AuthError(
                code=exc.response.status_code,
                message=str(exc),
            )
        return None, auth_error

    except requests.exceptions.RequestException as exc:
        return None, AuthError(
            code=500,
            message=f"Network error: {str(exc)}",
        )


def _normalize_refresh_response(response_data: Dict[str, Any]) -> SessionResponse:
    """
    Normalize Firebase token refresh response into SessionResponse.
    Firebase refresh endpoint returns different field names than sign-in.
    """
    expires_in = response_data.get("expires_in", response_data.get("expiresIn"))
    try:
        expires_in_seconds = int(expires_in) if expires_in else 3600
    except (ValueError, TypeError):
        expires_in_seconds = 3600

    return SessionResponse(
        local_id=response_data.get("user_id"),
        email=None,  # Refresh doesn't return email
        id_token=response_data.get("id_token"),
        refresh_token=response_data.get("refresh_token"),
        expires_in=expires_in_seconds,
        is_new_user=False,
        created_at=None,
    )


def should_refresh_session(
    token_created_at: float,
    expires_in_seconds: int,
    buffer_seconds: int = 300,
) -> bool:
    """
    Determine if a session should be refreshed based on time remaining.

    Args:
        token_created_at: Unix timestamp when token was created
        expires_in_seconds: Token lifetime in seconds
        buffer_seconds: Refresh buffer before actual expiration

    Returns:
        True if token should be refreshed
    """
    expiration_time = token_created_at + expires_in_seconds
    time_remaining = expiration_time - time.time()
    return time_remaining <= buffer_seconds


def refresh_and_validate(
    old_refresh_token: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Refresh a session and validate the new tokens.

    Args:
        old_refresh_token: The refresh token to use
        api_key: Firebase API key

    Returns:
        Dict with refresh result and validation status
    """
    session, error = refresh_session(
        refresh_token=old_refresh_token,
        api_key=api_key,
    )

    if not session:
        return {
            "success": False,
            "error": error.message if error else "Unknown error",
            "provider": "firebase_auth",
        }

    valid = bool(session.id_token and session.refresh_token and session.expires_in)

    return {
        "success": True,
        "provider": "firebase_auth",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "id_token": session.id_token,
        "refresh_token": session.refresh_token,
        "expires_in": session.expires_in,
        "user_id": session.local_id,
        "tokens_valid": valid,
    }


if __name__ == "__main__":
    import sys

    refresh_token = sys.argv[1] if len(sys.argv) > 1 else ""

    if not refresh_token:
        print("Usage: python refresh_session.py <refresh_token>")
        sys.exit(1)

    session, error = refresh_session(refresh_token=refresh_token)
    if session:
        print(f"Session refreshed: userId={session.local_id}, expiresIn={session.expires_in}")
    else:
        print(f"Refresh failed: {error.message}")
