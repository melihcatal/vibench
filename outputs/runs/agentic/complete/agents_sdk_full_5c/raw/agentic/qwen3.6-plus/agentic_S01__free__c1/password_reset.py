"""
Start a password reset flow for a local account using Firebase Authentication.
Provider: Firebase Auth (Google Cloud Identity Toolkit API)
"""

import os
import json
import requests
from typing import Dict, Any, Optional, Tuple

from identity_client import FirebaseIdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse, AuthError, normalize_email


FIREBASE_API_KEY = os.environ.get("FIREBASE_API_KEY", "")
FIREBASE_PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "")
FIREBASE_AUTH_DOMAIN = f"{FIREBASE_PROJECT_ID}.firebaseapp.com"
FIREBASE_IDENTITY_TOOLKIT_BASE = "https://identitytoolkit.googleapis.com/v1"
FIREBASE_PASSWORD_RESET_ENDPOINT = f"{FIREBASE_IDENTITY_TOOLKIT_BASE}/accounts:sendOobCode"


def start_password_reset(
    email: str,
    continue_url: Optional[str] = None,
    locale: Optional[str] = "en-US",
    api_key: Optional[str] = None,
) -> Tuple[Optional[PasswordResetResponse], Optional[AuthError]]:
    """
    Initiate a password reset flow for a Firebase Auth user.

    This sends a password reset email to the user with a link containing
    an out-of-band (OOB) code that can be used to complete the reset.

    Args:
        email: User email address
        continue_url: URL to redirect user after password reset
        locale: Locale for the reset email
        api_key: Firebase API key (falls back to FIREBASE_API_KEY env var)

    Returns:
        Tuple of (PasswordResetResponse, AuthError) - one will be None
    """
    key = api_key or FIREBASE_API_KEY
    if not key:
        return None, AuthError(
            code=400,
            message="Firebase API key not configured"
        )

    normalized_email = normalize_email(email)

    req = PasswordResetRequest(
        email=normalized_email,
        continue_url=continue_url,
        locale=locale,
    )

    url = f"{FIREBASE_PASSWORD_RESET_ENDPOINT}?key={key}"
    payload = req.to_firebase_payload()

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        reset_response = PasswordResetResponse.from_firebase_response(data)
        return reset_response, None

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


def build_reset_link(
    email: str,
    oob_code: str,
    continue_url: Optional[str] = None,
    project_id: Optional[str] = None,
) -> str:
    """
    Build the password reset link for direct use.

    Args:
        email: User email address
        oob_code: Out-of-band code from Firebase response
        continue_url: URL to redirect after reset
        project_id: Firebase project ID

    Returns:
        The password reset URL
    """
    pid = project_id or FIREBASE_PROJECT_ID
    base_url = f"https://{pid}.firebaseapp.com/__/auth/handler"

    params = {
        "mode": "resetPassword",
        "oobCode": oob_code,
        "apiKey": os.environ.get("FIREBASE_API_KEY", ""),
    }
    if continue_url:
        params["continueUrl"] = continue_url

    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    return f"{base_url}?{query_string}"


def initiate_password_reset_with_tracking(
    email: str,
    continue_url: Optional[str] = None,
    locale: Optional[str] = "en-US",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initiate password reset and return enriched response with tracking info.

    Args:
        email: User email address
        continue_url: URL to redirect user after password reset
        locale: Locale for the reset email
        api_key: Firebase API key

    Returns:
        Dict with reset initiation result
    """
    reset_response, error = start_password_reset(
        email=email,
        continue_url=continue_url,
        locale=locale,
        api_key=api_key,
    )

    if not reset_response:
        return {
            "success": False,
            "error": error.message if error else "Unknown error",
            "provider_error": error.provider_error if error else None,
            "provider": "firebase_auth",
        }

    reset_link = build_reset_link(
        email=email,
        oob_code=reset_response.oob_code or "",
        continue_url=continue_url,
    )

    return {
        "success": True,
        "provider": "firebase_auth",
        "project_id": os.environ.get("FIREBASE_PROJECT_ID", ""),
        "email": reset_response.email,
        "request_type": reset_response.request_type,
        "oob_code": reset_response.oob_code,
        "reset_link": reset_link,
    }


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else "user@example.com"
    continue_url = sys.argv[2] if len(sys.argv) > 2 else None

    result = initiate_password_reset_with_tracking(
        email=email,
        continue_url=continue_url,
    )
    if result["success"]:
        print(f"Password reset initiated for {result['email']}")
    else:
        print(f"Password reset failed: {result['error']}")
