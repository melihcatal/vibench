from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import requests


@dataclass(slots=True)
class OktaOIDCConfig:
    okta_domain: str
    client_id: str
    client_secret: str | None = None
    audience: str = "api://default"
    authorization_server_id: str = "default"

    @property
    def issuer(self) -> str:
        return f"https://{self.okta_domain}/oauth2/{self.authorization_server_id}"

    @property
    def authorization_endpoint(self) -> str:
        return f"{self.issuer}/v1/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"{self.issuer}/v1/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"{self.issuer}/v1/userinfo"


def load_okta_config() -> OktaOIDCConfig:
    return OktaOIDCConfig(
        okta_domain=os.environ["OKTA_DOMAIN"],
        client_id=os.environ["OKTA_CLIENT_ID"],
        client_secret=os.environ.get("OKTA_CLIENT_SECRET"),
        audience=os.environ.get("OKTA_AUDIENCE", "api://default"),
        authorization_server_id=os.environ.get("OKTA_AUTH_SERVER_ID", "default"),
    )


def build_basic_auth_header(client_id: str, client_secret: str) -> str:
    raw = f"{client_id}:{client_secret}".encode("utf-8")
    encoded = base64.b64encode(raw).decode("ascii")
    return f"Basic {encoded}"


def build_authorization_url(base_url: str, params: dict[str, Any]) -> str:
    return f"{base_url}?{urlencode(params)}"


def exchange_code_for_tokens(
    code: str,
    redirect_uri: str,
    code_verifier: str | None = None,
) -> dict[str, Any]:
    config = load_okta_config()
    data: dict[str, Any] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    headers = {"Accept": "application/json"}
    if config.client_secret:
        headers["Authorization"] = build_basic_auth_header(
            config.client_id, config.client_secret
        )
    else:
        data["client_id"] = config.client_id
    response = requests.post(
        config.token_endpoint, data=data, headers=headers, timeout=30
    )
    response.raise_for_status()
    return response.json()


def fetch_okta_userinfo(access_token: str) -> dict[str, Any]:
    config = load_okta_config()
    response = requests.get(
        config.userinfo_endpoint,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def generate_pkce_verifier(length: int = 64) -> str:
    return secrets.token_urlsafe(length)[:128]


def generate_pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def default_headers() -> dict[str, str]:
    return {"Accept": "application/json", "Content-Type": "application/json"}
