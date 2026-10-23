import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> PasswordResetResponse:
    """Start a password reset flow for a local account using Auth0."""
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")

    if not all([domain, client_id]):
        raise ValueError("Missing Auth0 environment variables")

    url = f"https://{domain}/dbconnections/change_password"

    payload = {
        "client_id": client_id,
        "email": email,
        "connection": "Username-Password-Authentication",
    }

    headers = {"content-type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            return PasswordResetResponse(
                success=True, message="Password reset email sent", provider="auth0"
            )
        else:
            return PasswordResetResponse(
                success=False,
                message=f"Failed to send reset email: {response.text}",
                provider="auth0",
            )
    except requests.exceptions.RequestException as e:
        raise Exception(f"Auth0 password reset failed: {str(e)}")
