import requests
import json
from dataclasses import asdict

from identity_client import FirebaseConfig
from identity_models import PasswordResetRequest, PasswordResetResponse

FIREBASE_PASSWORD_RESET_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
)


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    """
    Starts a password reset flow for a local account using Firebase Authentication REST API.
    """
    if not FirebaseConfig.API_KEY:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    params = {"key": FirebaseConfig.API_KEY}
    headers = {"Content-Type": "application/json"}
    payload = asdict(request)

    try:
        response = requests.post(
            FIREBASE_PASSWORD_RESET_URL,
            params=params,
            headers=headers,
            data=json.dumps(payload),
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        return PasswordResetResponse(email=data["email"])
    except requests.exceptions.RequestException as e:
        error_message = (
            e.response.json().get("error", {}).get("message", str(e))
            if e.response
            else str(e)
        )
        raise ValueError(f"Failed to initiate password reset: {error_message}")
