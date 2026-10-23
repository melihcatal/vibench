import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


AUTH0_DOMAIN_ENV = "AUTH0_DOMAIN"
AUTH0_CLIENT_ID_ENV = "AUTH0_CLIENT_ID"
AUTH0_CLIENT_SECRET_ENV = "AUTH0_CLIENT_SECRET"
AUTH0_REDIRECT_URI_ENV = "AUTH0_REDIRECT_URI"
AUTH0_AUDIENCE_ENV = "AUTH0_AUDIENCE"
AUTH0_SCOPE_ENV = "AUTH0_SCOPE"


@dataclass(frozen=True)
class IdentityClientConfig:
    domain: str
    client_id: str
    client_secret: Optional[str]
    redirect_uri: Optional[str]
    audience: Optional[str]
    scope: str


def load_identity_client_config(prefix: str = "AUTH0") -> IdentityClientConfig:
    domain = os.getenv(f"{prefix}_DOMAIN", "")
    client_id = os.getenv(f"{prefix}_CLIENT_ID", "")
    client_secret = os.getenv(f"{prefix}_CLIENT_SECRET")
    redirect_uri = os.getenv(f"{prefix}_REDIRECT_URI")
    audience = os.getenv(f"{prefix}_AUDIENCE")
    scope = os.getenv(f"{prefix}_SCOPE", "openid profile email")
    return IdentityClientConfig(
        domain=domain,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        audience=audience,
        scope=scope,
    )


def build_auth0_authorize_url(
    domain: str,
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    audience: Optional[str] = None,
    extra_params: Optional[Dict[str, str]] = None,
) -> str:
    params: Dict[str, str] = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
    }
    if nonce:
        params["nonce"] = nonce
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    if audience:
        params["audience"] = audience
    if extra_params:
        params.update({k: v for k, v in extra_params.items() if v is not None})
    return f"https://{domain}/authorize?{requests.compat.urlencode(params)}"


def build_auth0_token_url(domain: str) -> str:
    return f"https://{domain}/oauth/token"


def exchange_code_for_tokens(
    code: str,
    code_verifier: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    config: Optional[IdentityClientConfig] = None,
    timeout: float = 30.0,
) -> Dict[str, Any]:
    cfg = config or load_identity_client_config()
    if not cfg.domain or not cfg.client_id:
        raise ValueError("AUTH0_DOMAIN and AUTH0_CLIENT_ID are required")
    payload: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "client_id": cfg.client_id,
        "code": code,
    }
    if redirect_uri or cfg.redirect_uri:
        payload["redirect_uri"] = redirect_uri or cfg.redirect_uri
    if code_verifier:
        payload["code_verifier"] = code_verifier
    if cfg.client_secret:
        payload["client_secret"] = cfg.client_secret
    response = requests.post(
        build_auth0_token_url(cfg.domain),
        json=payload,
        headers={"content-type": "application/json"},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def get_bearer_userinfo(access_token: str, userinfo_url: str = "https://openidconnect.googleapis.com/v1/userinfo", timeout: float = 10.0) -> Dict[str, Any]:
    response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def merge_identity_claims(primary: Dict[str, Any], secondary: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    result = dict(secondary or {})
    result.update({k: v for k, v in primary.items() if v is not None})
    return result
