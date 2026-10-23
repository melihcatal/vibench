import os
from dataclasses import dataclass
from typing import Any, Dict

import requests


@dataclass
class Auth0Config:
    domain: str = os.environ.get("AUTH0_DOMAIN", "")
    client_id: str = os.environ.get("AUTH0_CLIENT_ID", "")
    client_secret: str = os.environ.get("AUTH0_CLIENT_SECRET", "")
    audience: str = os.environ.get("AUTH0_AUDIENCE", "")

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}/"


def auth0_authorize_url(
    cfg: Auth0Config, redirect_uri: str, state: str, code_challenge: str = ""
) -> str:
    url = f"https://{cfg.domain}/authorize"
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
    }
    if cfg.audience:
        params["audience"] = cfg.audience
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return requests.Request("GET", url, params=params).prepare().url or url


def auth0_token_endpoint(cfg: Auth0Config) -> str:
    return f"https://{cfg.domain}/oauth/token"


def auth0_userinfo_endpoint(cfg: Auth0Config) -> str:
    return f"https://{cfg.domain}/userinfo"


def post_form(url: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(url, data=data, timeout=20)
    response.raise_for_status()
    return response.json()
