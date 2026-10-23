# identity_client.py
# Local configuration and client helper utilities for Email/Password Account Lifecycle

import os
import requests

# Configuration for the chosen concrete provider - IBM Cloud App ID
APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
APPID_URL = os.getenv("IBM_APPID_URL")


def get_appid_token():
    """Obtain an access token from IBM Cloud App ID token endpoint."""
    token_url = f"{APPID_URL}/token"
    auth = (APPID_CLIENT_ID, APPID_CLIENT_SECRET)
    data = {"grant_type": "client_credentials"}
    response = requests.post(token_url, auth=auth, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


# Helper to call App ID protected endpoints
def call_appid_endpoint(path, method="POST", data=None):
    headers = {
        "Authorization": f"Bearer {get_appid_token()}",
        "Content-Type": "application/json",
    }
    url = f"{APPID_URL}/{path}"
    resp = requests.request(method, url, headers=headers, json=data)
    resp.raise_for_status()
    return resp.json()
