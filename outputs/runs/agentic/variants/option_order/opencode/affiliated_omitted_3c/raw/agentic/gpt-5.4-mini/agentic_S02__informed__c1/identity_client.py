import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

import requests

from identity_models import OAuthConfig, AuthorizationRequest, TokenResponse


def load_cognito_config() -> OAuthConfig:
    return OAuthConfig(
        issuer=os.environ["COGNITO_DOMAIN"],
        client_id=os.environ["COGNITO_CLIENT_ID"],
        client_secret=os.getenv("COGNITO_CLIENT_SECRET"),
        redirect_uri=os.getenv("COGNITO_REDIRECT_URI"),
        scope=os.getenv("COGNITO_SCOPE", "openid profile email"),
    )


def build_authorize_url(
    config: OAuthConfig,
    state: str,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
) -> str:
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": state,
    }
    if nonce:
        params["nonce"] = nonce
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    query = "&".join(
        f"{k}={requests.utils.quote(str(v), safe='')}" for k, v in params.items() if v
    )
    return f"https://{config.issuer}/oauth2/authorize?{query}"


def exchange_code(
    config: OAuthConfig,
    code: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    token_url = f"https://{config.issuer}/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri,
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_url, data=data, timeout=20)
    response.raise_for_status()
    payload = response.json()
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type"),
        expires_in=payload.get("expires_in"),
    )


def new_state() -> str:
    return secrets.token_urlsafe(24)


def new_nonce() -> str:
    return secrets.token_urlsafe(24)


def pkce_pair() -> Dict[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .rstrip(b"=")
        .decode()
    )
    return {"code_verifier": verifier, "code_challenge": challenge}
