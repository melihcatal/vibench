"""
Register a new email/password user account using Firebase Authentication.
Provider: Firebase Auth (Google Cloud Identity Toolkit API)
"""

import os
import json
import requests
from typing import Dict, Any, Optional, Tuple

from identity_client import FirebaseIdentityClient
from identity_models import RegistrationRequest, SessionResponse, AuthError


FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_IDENTITY_TOOLKIT_BASE = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_SIGN_UP_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/accounts:signUp"


def register_user(
    email: str,
    password: str,
    display_name: Optional[str] = None,
    locale: Optional[str] = "en-US",
    api_key: Optional[str] = None,
) -> Tuple[Optional[SessionResponse], Optional[AuthError]]:
    """
    Create a new email/password user account via Firebase Auth.

    Args:
        email: User email address
        password: User password
        display_name: Optional display name
        locale: User locale preference
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

    req = RegistrationRequest(
        email=email,
        password=password,
        display_name=display_name,
        locale=locale,
    )

    url = f"{FIREBASE_SIGN_UP_ENDPOINT}?key={key}"
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


def register_user_batch(
    users: list[dict],
    api_key: Optional[str] = None,
) -> list[dict]:
    """
    Register multiple users and collect results.

    Args:
        users: List of dicts with keys: email, password, optional display_name
        api_key: Firebase API key

    Returns:
        List of result dicts with success/error info
    """
    results = []
    for user_data in users:
        email = user_data.get("email", "")
        password = user_data.get("password", "")
        display_name = user_data.get("display_name")
        locale = user_data.get("locale", "en-US")

        session, error = register_user(
            email=email,
            password=password,
            display_name=display_name,
            locale=locale,
            api_key=api_key,
        )

        if session:
            results.append({
                "email": email,
                "success": True,
                "local_id": session.local_id,
            })
        else:
            results.append({
                "email": email,
                "success": False,
                "error": error.message if error else "Unknown error",
                "provider_error": error.provider_error if error else None,
            })

    return results


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else "newuser@example.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "SecureP@ss123!"

    session, error = register_user(email=email, password=password)
    if session:
        print(f"User registered: {session.email}, localId={session.local_id}")
    else:
        print(f"Registration failed: {error.message}")
