import os
from typing import Optional
import requests

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", "")

AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}" if AUTH0_DOMAIN else ""
AUTH0_AUTH_URL = f"{AUTH0_BASE_URL}/oauth/token"
AUTH0_DB_CONNECTIONS_URL = f"{AUTH0_BASE_URL}/dbconnections"
AUTH0_MANAGEMENT_URL = f"{AUTH0_BASE_URL}/api/v2"


def get_management_api_token() -> Optional[str]:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CLIENT_SECRET:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CLIENT_SECRET must be set"
        )
    payload = {
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials",
    }
    resp = requests.post(AUTH0_AUTH_URL, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json().get("access_token")


def create_auth0_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    return session


def build_auth_headers(
    access_token: Optional[str] = None, management_token: Optional[str] = None
) -> dict:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    if management_token:
        headers["Authorization"] = f"Bearer {management_token}"
    return headers


def validate_config():
    if not AUTH0_DOMAIN:
        raise ValueError("AUTH0_DOMAIN environment variable is required")
    if not AUTH0_CLIENT_ID:
        raise ValueError("AUTH0_CLIENT_ID environment variable is required")
