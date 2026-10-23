import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


@dataclass
class IdentityProviderConfig:
    provider_name: str
    issuer_url: str
    authorize_endpoint: str
    token_endpoint: str
    userinfo_endpoint: Optional[str]
    client_id: str
    client_secret: Optional[str]
    redirect_uri: str
    audience: Optional[str] = None

    @classmethod
    def from_env(cls) -> "IdentityProviderConfig":
        provider_name = os.getenv("OIDC_PROVIDER_NAME", "auth0")
        issuer_url = os.environ["OIDC_ISSUER_URL"]
        authorize_endpoint = os.getenv("OIDC_AUTHORIZE_ENDPOINT", issuer_url.rstrip("/") + "/authorize")
        token_endpoint = os.getenv("OIDC_TOKEN_ENDPOINT", issuer_url.rstrip("/") + "/oauth/token")
        userinfo_endpoint = os.getenv("OIDC_USERINFO_ENDPOINT") or issuer_url.rstrip("/") + "/userinfo"
        client_id = os.environ["OIDC_CLIENT_ID"]
        client_secret = os.getenv("OIDC_CLIENT_SECRET")
        redirect_uri = os.environ["OIDC_REDIRECT_URI"]
        audience = os.getenv("OIDC_AUDIENCE")
        return cls(
            provider_name=provider_name,
            issuer_url=issuer_url,
            authorize_endpoint=authorize_endpoint,
            token_endpoint=token_endpoint,
            userinfo_endpoint=userinfo_endpoint,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            audience=audience,
        )


def build_authorization_url(cfg: IdentityProviderConfig, redirect_uri: str, state: str, code_challenge: str, scope: str, nonce: Optional[str] = None, response_mode: Optional[str] = None) -> str:
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    if nonce:
        params["nonce"] = nonce
    if response_mode:
        params["response_mode"] = response_mode
    if cfg.audience:
        params["audience"] = cfg.audience
    return f"{cfg.authorize_endpoint}?{urlencode(params)}"


def exchange_authorization_code(cfg: IdentityProviderConfig, code: str, redirect_uri: str, code_verifier: str) -> Any:
    data = {
        "grant_type": "authorization_code",
        "client_id": cfg.client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }
    if cfg.client_secret:
        data["client_secret"] = cfg.client_secret
    if cfg.audience:
        data["audience"] = cfg.audience
    resp = requests.post(cfg.token_endpoint, data=data, timeout=30)
    resp.raise_for_status()
    return _TokenPayload.from_json(resp.json())


def fetch_userinfo(cfg: IdentityProviderConfig, access_token: str) -> Dict[str, Any]:
    if not cfg.userinfo_endpoint:
        return {}
    resp = requests.get(cfg.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    resp.raise_for_status()
    return resp.json()


def introspect_id_token(cfg: IdentityProviderConfig, id_token: str) -> Dict[str, Any]:
    return {"id_token": id_token, "issuer": cfg.issuer_url, "provider": cfg.provider_name}


@dataclass
class _TokenPayload:
    access_token: str
    id_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str
    expires_in: Optional[int]
    scope: Optional[str]
    claims: Dict[str, Any]

    @classmethod
    def from_json(cls, payload: Dict[str, Any]) -> "_TokenPayload":
        claims = payload.get("claims") or {}
        return cls(
            access_token=payload["access_token"],
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            token_type=payload.get("token_type", "Bearer"),
            expires_in=payload.get("expires_in"),
            scope=payload.get("scope"),
            claims=claims,
        )
