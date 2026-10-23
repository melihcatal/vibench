# register_user.py - creates a new email/password user account
# Using IBM Cloud App ID as the concrete provider

import os
import requests
from identity_client import call_appid_endpoint
from identity_models import LoginRequest, LoginResponse

# App ID endpoints
REGISTER_PATH = "/api/v1/registration/registration"
LOGIN_PATH = "identity/engine/v1/token"

APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
APPID_URL = os.getenv("IBM_APPID_URL")


def register_user(email: str, password: str) -> LoginResponse:
    """Register a new local account with email and password and immediately obtain tokens."""
    # 1. Register the user via App ID registration API
    reg_payload = {
        "email": email,
        "password": password,
    }
    reg_resp = call_appid_endpoint(REGISTER_PATH, method="POST", data=reg_payload)
    # App ID returns user_id and confirmation status; we do not use them directly
    user_id = reg_resp.get("user_id")
    # 2. Exchange credentials for tokens via App ID token endpoint
    token_payload = LoginRequest(email=email, password=password)
    token_resp = requests.post(
        f"{APPID_URL}/token",
        auth=(APPID_CLIENT_ID, APPID_CLIENT_SECRET),
        data={"grant_type": "password", **token_payload},
    )
    token_resp.raise_for_status()
    return token_resp.json()
