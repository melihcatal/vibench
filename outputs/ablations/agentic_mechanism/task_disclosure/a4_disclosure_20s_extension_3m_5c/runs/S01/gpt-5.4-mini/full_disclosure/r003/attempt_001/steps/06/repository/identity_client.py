import os
from dataclasses import dataclass
from typing import Optional

import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_CONNECTION = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_SCOPES = os.getenv("AUTH0_SCOPES", "openid profile email offline_access")


class IdentityConfigurationError(Exception):
    pass


@dataclass(frozen=True)
class IdentityClientConfig:
    domain: str
    client_id: str
    client_secret: str
    connection: str = "Username-Password-Authentication"
    audience: str = ""
    scopes: str = "openid profile email offline_access"


def load_identity_client_config(
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    scopes: Optional[str] = None,
) -> IdentityClientConfig:
    resolved_domain = domain if domain is not None else AUTH0_DOMAIN
    resolved_client_id = client_id if client_id is not None else AUTH0_CLIENT_ID
    resolved_client_secret = client_secret if client_secret is not None else AUTH0_CLIENT_SECRET
    resolved_connection = connection if connection is not None else AUTH0_CONNECTION
    resolved_audience = audience if audience is not None else AUTH0_AUDIENCE
    resolved_scopes = scopes if scopes is not None else AUTH0_SCOPES

    if not resolved_domain:
        raise IdentityConfigurationError("AUTH0_DOMAIN is required")
    if not resolved_client_id:
        raise IdentityConfigurationError("AUTH0_CLIENT_ID is required")
    if not resolved_client_secret:
        raise IdentityConfigurationError("AUTH0_CLIENT_SECRET is required")

    if not resolved_audience:
        resolved_audience = f"https://{resolved_domain}/api/v2/"

    return IdentityClientConfig(
        domain=resolved_domain,
        client_id=resolved_client_id,
        client_secret=resolved_client_secret,
        connection=resolved_connection,
        audience=resolved_audience,
        scopes=resolved_scopes,
    )


def auth0_url(config: IdentityClientConfig, path: str) -> str:
    return f"https://{config.domain}{path}"


def auth0_headers(access_token: Optional[str] = None) -> dict:
    headers = {"Content-Type": "application/json"}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def post_json(url: str, payload: dict, headers: Optional[dict] = None, timeout: int = 30) -> requests.Response:
    return requests.post(url, json=payload, headers=headers or {"Content-Type": "application/json"}, timeout=timeout)
