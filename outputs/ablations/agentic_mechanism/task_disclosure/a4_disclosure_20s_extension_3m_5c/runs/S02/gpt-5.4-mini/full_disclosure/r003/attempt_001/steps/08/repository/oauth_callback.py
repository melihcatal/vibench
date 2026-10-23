import os
import secrets
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_TOKEN_ENDPOINT_PATH = "/oauth/token"


@dataclass(frozen=True)
class OAuthCallbackRequest:
    code: str
    redirect_uri: str
    client_id: str
    client_secret: Optional[str] = None
    code_verifier: Optional[str] = None


@dataclass(frozen=True)
class OAuthTokenResponse:
    access_token: str
    token_type: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    expires_in: Optional[int]
    scope: Optional[str]
    raw: Dict[str, Any]


def _auth0_domain() -> str:
    domain = os.getenv(AUTH0_DOMAIN_ENV)
    if not domain:
        raise ValueError("AUTH0_DOMAIN is required")
    return domain.rstrip("/")


def _token_endpoint() -> str:
    return f"https://{_auth0_domain()}{AUTH0_TOKEN_ENDPOINT_PATH}"


def exchange_authorization_code(request: OAuthCallbackRequest) -> OAuthTokenResponse:
    payload = {
        "grant_type": "authorization_code",
        "client_id": request.client_id,
        "code": request.code,
        "redirect_uri": request.redirect_uri,
    }
    secret = request.client_secret or os.getenv(AUTH0_CLIENT_SECRET_ENV)
    if secret:
        payload["client_secret"] = secret
    if request.code_verifier:
        payload["code_verifier"] = request.code_verifier

    response = requests.post(
        _token_endpoint(),
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return OAuthTokenResponse(
        access_token=data["access_token"],
        token_type=data.get("token_type", "Bearer"),
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        expires_in=data.get("expires_in"),
        scope=data.get("scope"),
        raw=data,
    )


def handle_oauth_callback(code: str, state: Optional[str] = None, code_verifier: Optional[str] = None) -> OAuthTokenResponse:
    del state
    client_id = os.getenv(AUTH0_CLIENT_ID_ENV)
    redirect_uri = os.getenv(AUTH0_REDIRECT_URI_ENV)
    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID is required")
    if not redirect_uri:
        raise ValueError("AUTH0_REDIRECT_URI is required")
    request = OAuthCallbackRequest(
        code=code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        client_secret=os.getenv(AUTH0_CLIENT_SECRET_ENV),
        code_verifier=code_verifier,
    )
    return exchange_authorization_code(request)
