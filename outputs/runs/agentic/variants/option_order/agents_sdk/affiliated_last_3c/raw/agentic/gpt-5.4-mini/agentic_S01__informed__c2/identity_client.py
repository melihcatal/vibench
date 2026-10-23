from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

import requests

from identity_models import ensure_email, normalize_locale

AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_CONNECTION_ENV = "AUTH0_CONNECTION"
AUTH0_MGMT_TOKEN_ENV = "AUTH0_MGMT_TOKEN"

AUTH0_API_BASE = "https://{domain}/api/v2"
AUTH0_OIDC_BASE = "https://{domain}/oauth"


class IdentityClientError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session


def config() -> Dict[str, str]:
    domain = os.getenv(AUTH0_DOMAIN_ENV, "")
    client_id = os.getenv(AUTH0_CLIENT_ID_ENV, "")
    client_secret = os.getenv(AUTH0_CLIENT_SECRET_ENV, "")
    audience = os.getenv(AUTH0_AUDIENCE_ENV, f"{AUTH0_API_BASE.format(domain=domain)}/")
    connection = os.getenv(AUTH0_CONNECTION_ENV, "Username-Password-Authentication")
    mgmt_token = os.getenv(AUTH0_MGMT_TOKEN_ENV, "")
    return {
        "domain": domain,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience,
        "connection": connection,
        "mgmt_token": mgmt_token,
    }


def require_config() -> Dict[str, str]:
    cfg = config()
    if not cfg["domain"] or not cfg["client_id"]:
        raise IdentityClientError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    return cfg


def management_headers(token: Optional[str] = None) -> Dict[str, str]:
    cfg = require_config()
    bearer = token or cfg["mgmt_token"]
    if not bearer:
        raise IdentityClientError("AUTH0_MGMT_TOKEN is required for management operations")
    return {"Authorization": f"Bearer {bearer}"}


def oidc_token_headers() -> Dict[str, str]:
    return {"Content-Type": "application/x-www-form-urlencoded"}


def auth0_api_url(path: str) -> str:
    cfg = require_config()
    return AUTH0_API_BASE.format(domain=cfg["domain"]) + path


def auth0_oidc_url(path: str) -> str:
    cfg = require_config()
    return AUTH0_OIDC_BASE.format(domain=cfg["domain"]) + path


def client_credentials_token() -> str:
    cfg = require_config()
    if not cfg["client_secret"]:
        raise IdentityClientError("AUTH0_CLIENT_SECRET is required for client credentials")
    response = _session().post(
        auth0_oidc_url("/token"),
        headers=oidc_token_headers(),
        data={
            "grant_type": "client_credentials",
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "audience": cfg["audience"],
        },
        timeout=30,
    )
    if response.status_code >= 400:
        raise IdentityClientError(f"Auth0 token request failed: {response.text}")
    data = response.json()
    token = data.get("access_token")
    if not token:
        raise IdentityClientError("Auth0 token response missing access_token")
    return token


def management_token() -> str:
    cfg = config()
    return cfg["mgmt_token"] or client_credentials_token()


def request_json(method: str, url: str, *, headers: Optional[Dict[str, str]] = None, json: Optional[Dict[str, Any]] = None, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = _session().request(method, url, headers=headers, json=json, data=data, timeout=30)
    if response.status_code >= 400:
        raise IdentityClientError(f"Auth0 request failed ({response.status_code}): {response.text}")
    if not response.text:
        return {}
    return response.json()


def normalize_account_payload(email: str, password: str, locale: Optional[str] = None, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    payload = {
        "email": ensure_email(email),
        "password": password,
        "connection": require_config()["connection"],
    }
    if locale:
        payload["user_metadata"] = {"locale": normalize_locale(locale)}
    if extra:
        payload.update(extra)
    return payload
