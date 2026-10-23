"""
Sign in a user with email and password using Firebase Authentication.
Provider: Firebase Auth (Google Cloud Identity Toolkit API)
"""

import os
import json
import requests
from typing import Dict, Any, Optional, Tuple

from identity_client import FirebaseIdentityClient
from identity_models import LoginRequest, SessionResponse, AuthError, normalize_email


FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_IDENTITY_TOOLKIT_BASE = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_SIGN_IN_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/accounts:signInWithPassword"


def email_password_login(
    email: str,
    password: str,
    api_key: Optional[str] = None,
) -> Tuple[Optional[SessionResponse], Optional[AuthError]]:
    """
    Sign in a user with email and password via Firebase Auth.

    Args:
        email: User email address
        password: User password
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

    normalized_email = normalize_email(email)

    req = LoginRequest(
        email=normalized_email,
        password=password,
    )

    url = f"{FIREBASE_SIGN_IN_ENDPOINT}?key={key}"
    payload = req.to_firebase_payload()

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        session = SessionResponse.from_firebase_response(data)
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


def validate_session(session: SessionResponse) -> bool:
    """
    Validate that a session response contains required tokens.

    Args:
        session: SessionResponse from login

    Returns:
        True if session is valid
    """
    if not session:
        return False
    return bool(session.id_token and session.refresh_token and session.local_id)


def get_auth_headers(session: SessionResponse) -> Dict[str, str]:
    """
    Build authorization headers for authenticated requests.

    Args:
        session: SessionResponse with id_token

    Returns:
        Dict of headers to include in authenticated requests
    """
    return {
        "Authorization": f"Bearer {session.id_token}",
        "Content-Type": "application/json",
    }


def login_with_metadata(
    email: str,
    password: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Sign in and return enriched session metadata.

    Args:
        email: User email address
        password: User password
        api_key: Firebase API key

    Returns:
        Dict with session info and metadata
    """
    session, error = email_password_login(
        email=email,
        password=password,
        api_key=api_key,
    )

    if not session:
        return {
            "success": False,
            "error": error.message if error else "Unknown error",
            "provider": "firebase_auth",
        }

    return {
        "success": True,
        "provider": "firebase_auth",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "local_id": session.local_id,
        "email": session.email,
        "id_token": session.id_token,
        "refresh_token": session.refresh_token,
        "expires_in": session.expires_in,
        "is_new_user": session.is_new_user,
    }


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else "user@example.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "SecureP@ss123!"

    session, error = email_password_login(email=email, password=password)
    if session:
        print(f"Login successful: {session.email}, localId={session.local_id}")
    else:
        print(f"Login failed: {error.message}")
