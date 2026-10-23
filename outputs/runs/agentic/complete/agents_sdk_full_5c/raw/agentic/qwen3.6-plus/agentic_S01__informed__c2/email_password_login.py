"""Sign in a user with email and password and return tokens using Firebase Authentication."""

import os
import json
import requests
from identity_models import LoginRequest, LoginResponse


def get_rest_api_key() -> str:
    """Get the Firebase Web API key from environment variables."""
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "FIREBASE_WEB_API_KEY environment variable is required for REST-based sign in"
        )
    return api_key


def email_password_login(request: LoginRequest) -> LoginResponse:
    """Authenticate a user with email/password via Firebase Authentication REST API.

    Uses the Firebase Identity Toolkit REST API (identitytoolkit.googleapis.com)
    to sign in a user and return ID token, refresh token, and local ID (uid).

    Args:
        request: LoginRequest containing email and password.

    Returns:
        LoginResponse with id_token, refresh_token, uid, and expires_in duration.
    """
    api_key = get_rest_api_key()

    # Firebase Authentication REST API endpoint
    sign_in_url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    )

    payload = {
        "email": request.email,
        "password": request.password,
        "returnSecureToken": True,
    }

    response = requests.post(
        f"{sign_in_url}?key={api_key}",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        error_data = response.json()
        error_message = error_data.get("error", {}).get("message", "Unknown Firebase auth error")
        raise ValueError(f"Firebase Authentication failed: {error_message}")

    data = response.json()

    return LoginResponse(
        id_token=data["idToken"],
        refresh_token=data["refreshToken"],
        uid=data["localId"],
        expires_in=int(data["expiresIn"]),
        email=data.get("email", request.email),
    )
