from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Auth0Config:
    domain: str
    client_id: str
    client_secret: str | None = None
    audience: str | None = None
    redirect_path: str = "/callback"


def get_auth0_config() -> Auth0Config:
    return Auth0Config(
        domain=os.getenv("AUTH0_DOMAIN", "example.auth0.com"),
        client_id=os.getenv("AUTH0_CLIENT_ID", "example-client-id"),
        client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        audience=os.getenv("AUTH0_AUDIENCE"),
        redirect_path=os.getenv("AUTH0_REDIRECT_PATH", "/callback"),
    )


def build_redirect_uri(config: Auth0Config) -> str:
    base = os.getenv("AUTH0_REDIRECT_URI_BASE", "https://app.example.com")
    return base.rstrip("/") + config.redirect_path
