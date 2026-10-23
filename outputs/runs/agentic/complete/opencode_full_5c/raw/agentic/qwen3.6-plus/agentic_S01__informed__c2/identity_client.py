import os
import requests
from typing import Optional

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET", "")
AUTH0_MANAGEMENT_API_AUDIENCE = os.environ.get(
    "AUTH0_MANAGEMENT_API_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/"
)
AUTH0_API_AUDIENCE = os.environ.get("AUTH0_API_AUDIENCE", "")

AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
AUTH0_BASE_URL = f"https://{AUTH0_DOMAIN}"
AUTH0_MANAGEMENT_URL = f"https://{AUTH0_DOMAIN}/api/v2"
AUTH0_OAUTH_URL = f"https://{AUTH0_DOMAIN}/oauth/token"


def get_management_token(
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    audience: Optional[str] = None,
) -> str:
    d = domain or AUTH0_DOMAIN
    cid = client_id or AUTH0_CLIENT_ID
    csecret = client_secret or AUTH0_CLIENT_SECRET
    aud = audience or AUTH0_MANAGEMENT_API_AUDIENCE
    url = f"https://{d}/oauth/token"
    payload = {
        "client_id": cid,
        "client_secret": csecret,
        "audience": aud,
        "grant_type": "client_credentials",
    }
    resp = requests.post(url, json=payload, timeout=15)
    resp.raise_for_status()
    return resp.json()["access_token"]


def build_auth_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }


def build_management_url(path: str) -> str:
    return f"{AUTH0_MANAGEMENT_URL}/{path.lstrip('/')}"


def build_oauth_url() -> str:
    return AUTH0_OAUTH_URL


def build_login_payload(
    email: str,
    password: str,
    client_id: Optional[str] = None,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> dict:
    return {
        "grant_type": "password",
        "username": email.strip().lower(),
        "password": password,
        "client_id": client_id or AUTH0_CLIENT_ID,
        "audience": audience or AUTH0_API_AUDIENCE,
        "scope": scope or "openid profile email offline_access",
    }


def build_refresh_payload(
    refresh_token: str,
    client_id: Optional[str] = None,
    audience: Optional[str] = None,
    scope: Optional[str] = None,
) -> dict:
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id or AUTH0_CLIENT_ID,
        "refresh_token": refresh_token.strip(),
    }
    if audience:
        payload["audience"] = audience
    if scope:
        payload["scope"] = scope
    return payload
