import base64
import hashlib
import secrets
import urllib.parse
from dataclasses import dataclass
from typing import Dict, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_SCOPE_DEFAULT = "openid profile email offline_access"
AUTH0_AUTHORIZE_PATH = "/authorize"


@dataclass(frozen=True)
class PKCELoginConfig:
    domain: str
    client_id: str
    redirect_uri: str
    audience: Optional[str] = None
    scope: str = AUTH0_SCOPE_DEFAULT


@dataclass(frozen=True)
class PKCELoginState:
    authorization_url: str
    code_verifier: str
    code_challenge: str
    state: str


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def generate_code_verifier(length: int = 64) -> str:
    if length < 43 or length > 128:
        raise ValueError("PKCE code_verifier length must be between 43 and 128")
    return _b64url(secrets.token_bytes(length))[:length]


def generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("ascii")).digest()
    return _b64url(digest)


def build_authorization_url(config: PKCELoginConfig, state: Optional[str] = None) -> PKCELoginState:
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)
    state_value = state or secrets.token_urlsafe(32)
    params: Dict[str, str] = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": state_value,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if config.audience:
        params["audience"] = config.audience
    authorization_url = f"https://{config.domain}{AUTH0_AUTHORIZE_PATH}?{urllib.parse.urlencode(params)}"
    return PKCELoginState(
        authorization_url=authorization_url,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        state=state_value,
    )


def exchange_code_for_tokens(domain: str, client_id: str, redirect_uri: str, code: str, code_verifier: str) -> Dict[str, object]:
    token_url = f"https://{domain}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }
    response = requests.post(token_url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def start_pkce_login(domain: str, client_id: str, redirect_uri: str, audience: Optional[str] = None, scope: str = AUTH0_SCOPE_DEFAULT, state: Optional[str] = None) -> PKCELoginState:
    config = PKCELoginConfig(domain=domain, client_id=client_id, redirect_uri=redirect_uri, audience=audience, scope=scope)
    return build_authorization_url(config, state=state)
