# password_reset.py - starts a password reset flow for a local account
# Using IBM Cloud App ID as the concrete provider

import os
import requests
from identity_models import PasswordResetRequest, PasswordResetResponse

APPID_URL = os.getenv("IBM_APPID_URL")


def initiate_password_reset(email: str) -> PasswordResetResponse:
    """Request a password reset for the given email."""
    payload = {
        "email": email,
    }
    resp = requests.post(
        f"{APPID_URL}/api/v1/management/reset-password",
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()
