import os
import json
import time
import base64
import hashlib
import secrets
from typing import Optional
from urllib.parse import urlencode, urljoin

import requests
import jwt
from jwt import PyJWKClient

from identity_models import AuthRequest, TokenResponse, PKCEState


class IdentityConfig:
    def __init__(self):
        self.auth0_domain = os.environ.get("AUTH0_DOMAIN", "your-tenant.auth0.com")
        self.auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "")
        self.auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")
        self.auth0_audience = os.environ.get("AUTH0_AUDIENCE", "")
        self.redirect_uri = os.environ.get(
            "OAUTH_REDIRECT_URI", "http://localhost:3000/callback"
        )
        self.scope = os.environ.get("OAUTH_SCOPE", "openid profile email")
        self.connection = os.environ.get("AUTH0_CONNECTION", "")
        self.session_secret = os.environ.get("SESSION_SECRET", secrets.token_hex(32))
        self.cookie_max_age = int(os.environ.get("COOKIE_MAX_AGE", "86400"))

    @property
    def issuer(self) -> str:
        return f"https://{self.auth0_domain}"

    @property
    def authorize_url(self) -> str:
        return f"{self.issuer}/authorize"

    @property
    def token_url(self) -> str:
        return f"{self.issuer}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"{self.issuer}/userinfo"

    @property
    def jwks_url(self) -> str:
        return f"{self.issuer}/.well-known/jwks.json"

    @property
    def logout_url(self) -> str:
        return f"{self.issuer}/v2/logout"

    def validate(self) -> list[str]:
        errors = []
        if not self.auth0_domain or self.auth0_domain == "your-tenant.auth0.com":
            errors.append("AUTH0_DOMAIN must be set to a valid Auth0 tenant domain")
        if not self.auth0_client_id:
            errors.append("AUTH0_CLIENT_ID must be set")
        if not self.auth0_client_secret:
            errors.append("AUTH0_CLIENT_SECRET must be set")
        if not self.redirect_uri:
            errors.append("OAUTH_REDIRECT_URI must be set")
        return errors


_config: Optional[IdentityConfig] = None


def get_config() -> IdentityConfig:
    global _config
    if _config is None:
        _config = IdentityConfig()
    return _config


def reset_config() -> None:
    global _config
    _config = None


def build_authorize_url(
    config: Optional[IdentityConfig] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    connection: Optional[str] = None,
    audience: Optional[str] = None,
    prompt: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> str:
    cfg = config or get_config()
    request = AuthRequest(
        client_id=cfg.auth0_client_id,
        redirect_uri=redirect_uri or cfg.redirect_uri,
        scope=scope or cfg.scope,
        connection=connection or cfg.connection or None,
        audience=audience or cfg.audience or None,
        prompt=prompt,
    )
    params = request.to_query_params()
    if extra_params:
        params.update(extra_params)
    return f"{cfg.authorize_url}?{urlencode(params)}"


def exchange_code_for_tokens(
    authorization_code: str,
    redirect_uri: Optional[str] = None,
    code_verifier: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> TokenResponse:
    cfg = config or get_config()
    token_data = {
        "grant_type": "authorization_code",
        "client_id": cfg.auth0_client_id,
        "client_secret": cfg.auth0_client_secret,
        "code": authorization_code,
        "redirect_uri": redirect_uri or cfg.redirect_uri,
    }
    if code_verifier:
        token_data["code_verifier"] = code_verifier
    response = requests.post(
        cfg.token_url,
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    return TokenResponse.from_dict(response.json())


def fetch_userinfo(
    access_token: str,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    response = requests.get(
        cfg.userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def verify_id_token(
    id_token: str,
    config: Optional[IdentityConfig] = None,
    nonce: Optional[str] = None,
) -> dict:
    cfg = config or get_config()
    jwks_client = PyJWKClient(cfg.jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    payload = jwt.decode(
        id_token,
        signing_key.key,
        algorithms=["RS256"],
        audience=cfg.auth0_client_id,
        issuer=cfg.issuer,
        options={"verify_nonce": nonce is not None},
    )
    if nonce and payload.get("nonce") != nonce:
        raise ValueError("Nonce mismatch: token nonce does not match expected value")
    return payload


def validate_state(expected_state: str, received_state: str) -> bool:
    return secrets.compare_digest(expected_state, received_state)


def generate_session_id() -> str:
    return secrets.token_urlsafe(32)


def extract_ip_address(request_headers: dict) -> Optional[str]:
    for header in ["X-Forwarded-For", "X-Real-IP", "CF-Connecting-IP"]:
        if header in request_headers:
            value = request_headers[header]
            return value.split(",")[0].strip()
    return None


def extract_user_agent(request_headers: dict) -> Optional[str]:
    return request_headers.get("User-Agent")


def sanitize_claims(claims: dict) -> dict:
    sensitive_keys = {"access_token", "refresh_token", "id_token", "client_secret"}
    return {k: v for k, v in claims.items() if k not in sensitive_keys}


def build_logout_url(
    return_to: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> str:
    cfg = config or get_config()
    params = {"client_id": cfg.auth0_client_id}
    if return_to:
        params["returnTo"] = return_to
    return f"{cfg.logout_url}?{urlencode(params)}"
