import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set.")

    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"requestType": "PASSWORD_RESET", "email": request.email}

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # The response for sendOobCode is minimal, usually just the email sent to.
        # We return a generic success message.
        return PasswordResetResponse(
            message=f"Password reset email sent to {request.email}"
        )
    except requests.exceptions.RequestException as e:
        error_message = response.json().get("error", {}).get("message", str(e))
        raise RuntimeError(f"Failed to send password reset email: {error_message}")
