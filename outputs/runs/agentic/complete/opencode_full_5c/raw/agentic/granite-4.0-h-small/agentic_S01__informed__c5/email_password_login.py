# email_password_login.py - signs in a user with email and password and returns tokens
# Using IBM Cloud App ID as the concrete provider

import os
import requests
from identity_client import call_appid_endpoint
from identity_models import LoginRequest, LoginResponse

APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
APPID_URL = os.getenv("IBM_APPID_URL")


def login_user(email: str, password: str) -> LoginResponse:
    """Authenticate with email/password and return tokens."""
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "scope": "openid",
    }
    resp = requests.post(
        f"{APPID_URL}/token",
        auth=(APPID_CLIENT_ID, APPID_CLIENT_SECRET),
        data=payload,
    )
    resp.raise_for_status()
    return resp.json()
