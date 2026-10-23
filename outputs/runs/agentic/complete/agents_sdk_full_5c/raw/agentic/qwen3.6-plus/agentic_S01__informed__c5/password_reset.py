"""
password_reset.py
Starts a password reset flow for a local account via IBM Cloud App ID.

Provider: IBM Cloud App ID (requests / REST)
Auth: IBM_APPID_CLIENT_ID, IBM_APPID_CLIENT_SECRET
"""

import os
import requests
from identity_client import get_appid_config, get_appid_token
from identity_models import PasswordResetRequest, PasswordResetResponse


def initiate_password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    """
    Initiates a password reset flow for a user in IBM Cloud App ID.
    Sends a password reset email to the user's registered email address.

    Args:
        request: PasswordResetRequest containing the user's email.

    Returns:
        PasswordResetResponse with reset status and details.
    """
    config = get_appid_config()
    appid_token = get_appid_token()
    tenant_id = config.get("tenant_id", "")
    region = config.get("region", "us")

    api_url = (
        f"https://{region}.appid.cloud.ibm.com/management/v4/{tenant_id}"
        "/cloud_directory/users/forgot_password"
    )

    headers = {
        "Authorization": f"Bearer {appid_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "email": request.email,
        "redirect_url": request.redirect_url,
    }

    response = requests.post(api_url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    result = response.json()

    return PasswordResetResponse(
        success=True,
        email=request.email,
        message="Password reset email sent successfully.",
        cloud_directory_user_id=result.get("uuid"),
    )


if __name__ == "__main__":
    req = PasswordResetRequest(
        email="user@example.com",
        redirect_url="https://myapp.example.com/reset-password",
    )
    resp = initiate_password_reset(req)
    print(f"Password reset initiated for {resp.email}: {resp.message}")
