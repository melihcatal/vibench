# refresh_session.py - refreshes an expired session or access token
# Using IBM Cloud App ID as the concrete provider

import os
import requests
from identity_client import call_appid_endpoint
from identity_models import RefreshRequest, RefreshResponse

APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
APPID_URL = os.getenv("IBM_APPID_URL")


def refresh_access_token(refresh_token: str) -> RefreshResponse:
    """Refresh an expired access token using the stored refresh token."""
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "openid",
    }
    resp = requests.post(
        f"{APPID_URL}/token",
        auth=(APPID_CLIENT_ID, APPID_CLIENT_SECRET),
        data=payload,
    )
    resp.raise_for_status()
    return resp.json()
