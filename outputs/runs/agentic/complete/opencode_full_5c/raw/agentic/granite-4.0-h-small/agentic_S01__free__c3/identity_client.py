# [HELPER] identity_client.py
# Local configuration and client helper utilities for Email/Password Account Lifecycle

# Provider: Auth0 (concrete email/password identity service)

import os
import json
import requests
from typing import Any, Dict

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-auth0-domain.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")

BASE_URL = f"https://{AUTH0_DOMAIN}"

HEADERS = {"Content-Type": "application/json"}


def get_management_token() -> str:
    """Fetch a Management API token using client credentials."""
    token_endpoint = f"{BASE_URL}/oauth/token"
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": f"{BASE_URL}/api/v2/",
        "grant_type": "client_credentials",
    }
    resp = requests.post(token_endpoint, data=payload)
    resp.raise_for_status()
    return resp.json()["access_token"]


def call_management_api(
    endpoint: str, method: str = "GET", payload: Any = None
) -> Dict:
    """Generic helper to call any Auth0 Management API endpoint."""
    token = get_management_token()
    url = f"{BASE_URL}{endpoint}"
    if method.upper() == "GET":
        resp = requests.get(
            url, headers={**HEADERS, "Authorization": f"Bearer {token}"}
        )
    elif method.upper() == "POST":
        resp = requests.post(
            url, headers={**HEADERS, "Authorization": f"Bearer {token}"}, json=payload
        )
    else:
        raise ValueError(f"Unsupported method {method}")
    resp.raise_for_status()
    return resp.json()


def register_user(
    email: str, password: str, connection: str = "Username-Password-Authentication"
) -> Dict:
    """Convenient wrapper around /users creation."""
    endpoint = "/api/v2/users"
    payload = {
        "email": email,
        "password": password,
        "connection": connection,
        "email_verified": False,
        "user_metadata": {},
    }
    return call_management_api(endpoint, method="POST", payload=payload)


# Additional helpers can be added here as needed (e.g., get_user, update_user, etc.)
