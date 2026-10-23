import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class FederatedLoginConfig:
    issuer_url: str
    client_id: str
    redirect_uri: str
    audience: Optional[str] = None
    scope: str = "openid profile email"


def load_federated_login_config() -> FederatedLoginConfig:
    issuer_url = os.environ["OIDC_ISSUER_URL"].rstrip("/")
    client_id = os.environ["OIDC_CLIENT_ID"]
    redirect_uri = os.environ["OIDC_REDIRECT_URI"]
    audience = os.getenv("OIDC_AUDIENCE")
    scope = os.getenv("OIDC_SCOPE", "openid profile email")
    return FederatedLoginConfig(
        issuer_url=issuer_url,
        client_id=client_id,
        redirect_uri=redirect_uri,
        audience=audience,
        scope=scope,
    )


@lru_cache(maxsize=1)
def get_oidc_metadata(issuer_url: Optional[str] = None) -> Dict[str, Any]:
    base = issuer_url or load_federated_login_config().issuer_url
    response = requests.get(f"{base}/.well-known/openid-configuration", timeout=10)
    response.raise_for_status()
    return response.json()


def build_authorization_url(state: str, nonce: str) -> str:
    config = load_federated_login_config()
    metadata = get_oidc_metadata(config.issuer_url)
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": config.scope,
        "state": state,
        "nonce": nonce,
    }
    if config.audience:
        params["audience"] = config.audience
    from urllib.parse import urlencode

    return f"{metadata['authorization_endpoint']}?{urlencode(params)}"


def exchange_code_for_tokens(code: str) -> Dict[str, Any]:
    config = load_federated_login_config()
    metadata = get_oidc_metadata(config.issuer_url)
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
    }
    response = requests.post(metadata["token_endpoint"], data=data, timeout=10)
    response.raise_for_status()
    return response.json()


def refresh_access_token(refresh_token: str) -> Dict[str, Any]:
    config = load_federated_login_config()
    metadata = get_oidc_metadata(config.issuer_url)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": config.client_id,
    }
    response = requests.post(metadata["token_endpoint"], data=data, timeout=10)
    response.raise_for_status()
    return response.json()
