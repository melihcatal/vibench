import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    """Initiate password reset flow for a user using Auth0."""
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    # Auth0 password reset endpoint
    reset_url = f"https://{domain}/dbconnections/change_password"

    payload = {
        "client_id": client_id,
        "email": email,
        "connection": "Username-Password-Authentication",
    }

    response = requests.post(reset_url, json=payload)

    # Auth0 returns 200 even if email doesn't exist (for security)
    if response.status_code == 200:
        return PasswordResetResponse(
            success=True,
            message="If an account exists with this email, a password reset link has been sent.",
        )
    else:
        response.raise_for_status()
        return PasswordResetResponse(
            success=False, message="Failed to initiate password reset."
        )
