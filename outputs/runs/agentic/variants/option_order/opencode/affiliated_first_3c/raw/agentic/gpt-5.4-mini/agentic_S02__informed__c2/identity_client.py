import os
from dataclasses import dataclass
from typing import Dict, Optional

import requests


@dataclass
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: Optional[str]
    auth0_audience: Optional[str]


def load_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
        auth0_audience=os.environ.get("AUTH0_AUDIENCE"),
    )


def discovery_document(domain: str) -> Dict[str, str]:
    return requests.get(
        f"https://{domain}/.well-known/openid-configuration", timeout=10
    ).json()


def build_authorize_url(domain: str, params: Dict[str, str]) -> str:
    from urllib.parse import urlencode

    return f"https://{domain}/authorize?{urlencode(params)}"


def exchange_code(domain: str, payload: Dict[str, str]) -> Dict:
    return requests.post(
        f"https://{domain}/oauth/token", json=payload, timeout=10
    ).json()


def userinfo(domain: str, access_token: str) -> Dict:
    return requests.get(
        f"https://{domain}/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    ).json()
