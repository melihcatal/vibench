import base64
import hashlib
import json
import os
import secrets
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional

from identity_models import AuthorizationRequest, IdentityProviderConfig, TokenSet


def load_google_config() -> IdentityProviderConfig:
    return IdentityProviderConfig(
        issuer="https://accounts.google.com",
        client_id=os.environ.get("GOOGLE_CLIENT_ID", ""),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
        redirect_uri=os.environ.get("GOOGLE_REDIRECT_URI"),
        authorization_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
        token_endpoint="https://oauth2.googleapis.com/token",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        scope=os.environ.get("GOOGLE_SCOPE", "openid email profile"),
    )


def generate_state() -> str:
    return secrets.token_urlsafe(32)


def generate_nonce() -> str:
    return secrets.token_urlsafe(32)


def generate_pkce_pair() -> tuple[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return verifier, challenge


def build_authorization_url(config: IdentityProviderConfig, auth_request: AuthorizationRequest) -> str:
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": config.scope,
        "state": auth_request.state,
        "nonce": auth_request.nonce,
    }
    if auth_request.redirect_uri or config.redirect_uri:
        params["redirect_uri"] = auth_request.redirect_uri or config.redirect_uri
    if auth_request.code_challenge:
        params["code_challenge"] = auth_request.code_challenge
        params["code_challenge_method"] = auth_request.code_challenge_method or "S256"
    return f"{config.authorization_endpoint}?{urllib.parse.urlencode(params)}"


def exchange_code_for_tokens(config: IdentityProviderConfig, code: str, redirect_uri: Optional[str] = None, code_verifier: Optional[str] = None) -> TokenSet:
    data: Dict[str, Any] = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": config.client_id,
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    if redirect_uri or config.redirect_uri:
        data["redirect_uri"] = redirect_uri or config.redirect_uri
    if code_verifier:
        data["code_verifier"] = code_verifier
    req = urllib.request.Request(
        config.token_endpoint,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        payload = json.loads(resp.read().decode())
    return TokenSet(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )


def fetch_userinfo(config: IdentityProviderConfig, access_token: str) -> Dict[str, Any]:
    req = urllib.request.Request(config.userinfo_endpoint, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode())
