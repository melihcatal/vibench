import os
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN = os.environ["AUTH0_DOMAIN"]
AUTH0_CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
AUTH0_CONNECTION = os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")


def _auth0_url(path: str) -> str:
    return f"https://{AUTH0_DOMAIN}{path}"


def _post(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    if response.content:
        return response.json()
    return {}


def register_user(email: str, password: str) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "client_id": AUTH0_CLIENT_ID,
        "email": email,
        "password": password,
        "connection": AUTH0_CONNECTION,
    }
    return _post(_auth0_url("/dbconnections/signup"), payload)


def sign_in_with_email_password(email: str, password: str) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "client_id": AUTH0_CLIENT_ID,
        "username": email,
        "password": password,
        "realm": AUTH0_CONNECTION,
    }
    if AUTH0_AUDIENCE:
        payload["audience"] = AUTH0_AUDIENCE
    return _post(_auth0_url("/oauth/token"), payload)


def start_password_reset(email: str) -> Dict[str, Any]:
    response = requests.post(
        _auth0_url("/dbconnections/change_password"),
        headers={"content-type": "application/json"},
        json={"client_id": AUTH0_CLIENT_ID, "email": email, "connection": AUTH0_CONNECTION},
        timeout=30,
    )
    response.raise_for_status()
    return {"message": response.text}


def refresh_session(refresh_token: str, client_secret: Optional[str] = None) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    if client_secret is None:
        client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
    if client_secret:
        payload["client_secret"] = client_secret
    return _post(_auth0_url("/oauth/token"), payload)
