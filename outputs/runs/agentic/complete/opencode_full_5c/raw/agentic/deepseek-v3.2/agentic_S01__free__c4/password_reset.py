import os
import requests
from identity_client import get_firebase_config
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    """
    Starts a password reset flow for a local account using Firebase Authentication.
    """
    config = get_firebase_config()
    api_key = config["api_key"]

    url = (
        f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    )

    payload = {"requestType": "PASSWORD_RESET", "email": email}

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

    data = response.json()

    return PasswordResetResponse(
        email=data["email"],
        request_type=data.get("requestType", "PASSWORD_RESET"),
        success=True,
        message="Password reset email sent successfully",
    )
