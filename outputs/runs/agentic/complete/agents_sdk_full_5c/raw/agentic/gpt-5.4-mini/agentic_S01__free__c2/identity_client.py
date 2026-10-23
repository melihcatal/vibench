from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class IdentityConfig:
    domain: str
    client_id: str
    client_secret: str
    audience: str
    connection_name: str
    timeout_seconds: float = 15.0


def get_identity_config() -> IdentityConfig:
    return IdentityConfig(
        domain=os.environ["AUTH0_DOMAIN"],
        client_id=os.environ["AUTH0_CLIENT_ID"],
        client_secret=os.environ["AUTH0_CLIENT_SECRET"],
        audience=os.environ.get("AUTH0_AUDIENCE", f"https://{os.environ['AUTH0_DOMAIN']}/api/v2/"),
        connection_name=os.environ.get("AUTH0_CONNECTION", "Username-Password-Authentication"),
        timeout_seconds=float(os.environ.get("AUTH0_TIMEOUT_SECONDS", "15")),
    )


def resolve_base_url(cfg: IdentityConfig) -> str:
    return f"https://{cfg.domain}"


def make_headers(cfg: IdentityConfig) -> Dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {cfg.client_secret}",
        "X-Auth0-Client": cfg.client_id,
    }
