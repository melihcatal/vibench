# [SAME-SCENARIO] password_reset.py - starts a password reset flow for a local account
# Provider: Google Firebase Authentication

import requests
from identity_client import FIREBASE_WEB_API_KEY
from identity_models import PasswordResetRequest, PasswordResetResponse

FIREBASE_PASSWORD_RESET_URL = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key="

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("Firebase Web API Key not found. Please set FIREBASE_API_KEY environment variable.")

    url = f"{FIREBASE_PASSWORD_RESET_URL}{FIREBASE_WEB_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "requestType": "PASSWORD_RESET",
        "email": request.email
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status() # Raise an exception for HTTP errors

    data = response.json()
    return PasswordResetResponse(
        email=data["email"]
    )
