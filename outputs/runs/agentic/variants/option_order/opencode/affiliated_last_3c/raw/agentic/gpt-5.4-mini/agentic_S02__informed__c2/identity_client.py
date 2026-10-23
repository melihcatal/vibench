import base64
import hashlib
import os
import secrets
from typing import Any, Dict, Optional

import requests

from identity_models import AuthorizationRequest, OAuthConfig


def load_oidc_config() -> OAuthConfig:
    issuer = os.getenv("AUTH0_DOMAIN", "https://example.auth0.com").rstrip("/")
    client_id = os.getenv("AUTH0_CLIENT_ID", "")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    redirect_uri = os.getenv("AUTH0_REDIRECT_URI")
    return OAuthConfig(
        issuer=issuer,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
    )


def discovery_document(issuer: str) -> Dict[str, Any]:
    return requests.get(f"{issuer}/.well-known/openid-configuration", timeout=15).json()


def build_authorization_request() -> AuthorizationRequest:
    verifier = secrets.token_urlsafe(48)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return AuthorizationRequest(
        state=secrets.token_urlsafe(24),
        nonce=secrets.token_urlsafe(24),
        code_verifier=verifier,
        code_challenge=challenge,
    )


def token_exchange(
    token_endpoint: str,
    config: OAuthConfig,
    code: str,
    redirect_uri: str,
    code_verifier: Optional[str] = None,
) -> Dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }
    return requests.post(
        token_endpoint,
        data={k: v for k, v in data.items() if v is not None},
        timeout=15,
    ).json()
