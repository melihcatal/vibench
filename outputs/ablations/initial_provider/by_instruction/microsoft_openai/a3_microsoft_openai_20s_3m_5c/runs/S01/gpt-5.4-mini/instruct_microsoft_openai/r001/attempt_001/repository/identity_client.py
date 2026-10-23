import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: Optional[str]
    auth0_audience: Optional[str]
    auth0_connection: Optional[str]


def load_identity_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        auth0_audience=os.getenv("AUTH0_AUDIENCE"),
        auth0_connection=os.getenv("AUTH0_CONNECTION"),
    )


def auth0_base_url(config: IdentityConfig) -> str:
    return f"https://{config.auth0_domain}"


def auth0_headers() -> Dict[str, str]:
    return {"content-type": "application/json"}


def post_auth0(path: str, json: Dict[str, Any], config: Optional[IdentityConfig] = None) -> Dict[str, Any]:
    cfg = config or load_identity_config()
    response = requests.post(f"{auth0_base_url(cfg)}{path}", json=json, headers=auth0_headers(), timeout=30)
    response.raise_for_status()
    return response.json()
