from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from authlib.integrations.requests_client import OAuth2Session


@dataclass(frozen=True)
class IdentityProviderConfig:
    issuer_url: str
    client_id: str
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    scope: str = "openid profile email"


def load_identity_config() -> IdentityProviderConfig:
    return IdentityProviderConfig(
        issuer_url=os.environ["OIDC_ISSUER_URL"],
        client_id=os.environ["OIDC_CLIENT_ID"],
        client_secret=os.environ.get("OIDC_CLIENT_SECRET"),
        redirect_uri=os.environ.get("OIDC_REDIRECT_URI"),
        scope=os.environ.get("OIDC_SCOPE", "openid profile email"),
    )


def oauth_session(config: IdentityProviderConfig, state: Optional[str] = None, code_verifier: Optional[str] = None) -> OAuth2Session:
    session = OAuth2Session(
        client_id=config.client_id,
        client_secret=config.client_secret,
        scope=config.scope,
        state=state,
        redirect_uri=config.redirect_uri,
        code_verifier=code_verifier,
    )
    return session
