from __future__ import annotations

import base64
import hashlib
import os
import secrets
from dataclasses import dataclass
from typing import Dict, Optional

from identity_models import OAuthConfig


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_CALLBACK_URL_ENV = "AUTH0_CALLBACK_URL"
AUTH0_ISSUER_ENV = "AUTH0_ISSUER"


@dataclass(frozen=True)
class IdentityClientConfig:
    domain: str
    client_id: str
    client_secret: Optional[str]
    audience: Optional[str]
    callback_url: str
    issuer: str

    @property
    def authorization_endpoint(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"

    @property
    def jwks_uri(self) -> str:
        return f"https://{self.domain}/.well-known/jwks.json"



def load_identity_client_config() -> IdentityClientConfig:
    domain = os.environ.get(AUTH0_DOMAIN_ENV, "example.us.auth0.com")
    client_id = os.environ.get(AUTH0_CLIENT_ID_ENV, "example-client-id")
    client_secret = os.environ.get(AUTH0_CLIENT_SECRET_ENV)
    audience = os.environ.get(AUTH0_AUDIENCE_ENV)
    callback_url = os.environ.get(AUTH0_CALLBACK_URL_ENV, "https://app.example.com/oauth/callback")
    issuer = os.environ.get(AUTH0_ISSUER_ENV, f"https://{domain}/")
    return IdentityClientConfig(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        audience=audience,
        callback_url=callback_url,
        issuer=issuer,
    )



def build_oauth_config(scopes: list[str] | None = None) -> OAuthConfig:
    cfg = load_identity_client_config()
    return OAuthConfig(
        authorization_endpoint=cfg.authorization_endpoint,
        token_endpoint=cfg.token_endpoint,
        userinfo_endpoint=cfg.userinfo_endpoint,
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
        redirect_uri=cfg.callback_url,
        audience=cfg.audience,
        scopes=scopes or ["openid", "profile", "email"],
    )



def generate_state() -> str:
    return secrets.token_urlsafe(24)



def generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)



def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")



def normalize_claims(raw: Dict[str, object]) -> Dict[str, object]:
    return {k: v for k, v in raw.items() if v not in (None, "")}
