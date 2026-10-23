import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional

import requests


@dataclass
class IdentityClientConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: str = ""
    issuer: str = ""
    redirect_uri: str = "http://localhost/callback"


def load_config() -> IdentityClientConfig:
    return IdentityClientConfig(
        auth0_domain=os.environ.get("AUTH0_DOMAIN", "example.auth0.com"),
        auth0_client_id=os.environ.get("AUTH0_CLIENT_ID", "client-id"),
        auth0_client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
        issuer=os.environ.get(
            "AUTH0_ISSUER",
            f"https://{os.environ.get('AUTH0_DOMAIN', 'example.auth0.com')}/",
        ),
        redirect_uri=os.environ.get("AUTH0_REDIRECT_URI", "http://localhost/callback"),
    )


def auth0_authorize_url(
    config: IdentityClientConfig,
    state: str,
    nonce: str,
    scope: str = "openid profile email",
) -> str:
    return (
        f"https://{config.auth0_domain}/authorize?response_type=code"
        f"&client_id={config.auth0_client_id}&redirect_uri={config.redirect_uri}"
        f"&scope={scope}&state={state}&nonce={nonce}"
    )


def token_endpoint(config: IdentityClientConfig) -> str:
    return f"https://{config.auth0_domain}/oauth/token"


def userinfo_endpoint(config: IdentityClientConfig) -> str:
    return f"https://{config.auth0_domain}/userinfo"


def exchange_code_for_tokens(
    config: IdentityClientConfig, code: str, code_verifier: Optional[str] = None
) -> Dict[str, str]:
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.auth0_client_id,
        "client_secret": config.auth0_client_secret,
        "code": code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(config), json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def generate_state() -> str:
    return secrets.token_urlsafe(24)


def generate_nonce() -> str:
    return secrets.token_urlsafe(24)


def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def pkce_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
