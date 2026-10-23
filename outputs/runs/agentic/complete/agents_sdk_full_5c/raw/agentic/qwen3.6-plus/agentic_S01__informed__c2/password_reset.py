"""Start a password reset flow for a local account using Firebase Authentication."""

import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse


def get_rest_api_key() -> str:
    """Get the Firebase Web API key from environment variables."""
    api_key = os.environ.get("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "FIREBASE_WEB_API_KEY environment variable is required for password reset"
        )
    return api_key


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    """Initiate a password reset email via Firebase Authentication REST API.

    Uses the Firebase Identity Toolkit REST API (identitytoolkit.googleapis.com)
    to send a password reset email to the user's registered email address.
    The user receives a link with an oobCode that can be used to set a new password.

    Args:
        request: PasswordResetRequest containing the email address for the account.

    Returns:
        PasswordResetResponse with the email the reset was sent to.
    """
    api_key = get_rest_api_key()

    # Firebase Identity Toolkit password reset endpoint
    reset_url = (
        "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
    )

    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email,
    }

    if request.continue_url:
        payload["continueUrl"] = request.continue_url

    if request.locale:
        payload["locale"] = request.locale

    response = requests.post(
        f"{reset_url}?key={api_key}",
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Reset request failed")
        except Exception:
            error_msg = f"Reset request failed with status {response.status_code}"
        raise ValueError(f"Firebase password reset error: {error_msg}")

    data = response.json()

    return PasswordResetResponse(
        email=data.get("email", request.email),
    )
