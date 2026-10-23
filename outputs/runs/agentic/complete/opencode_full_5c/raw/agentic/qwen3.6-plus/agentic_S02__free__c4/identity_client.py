import os
import json
import base64
import hashlib
import secrets
import requests
from typing import Optional, Dict, Any, Tuple
from identity_models import (
    OAuthConfig,
    PKCEConfig,
    TokenResponse,
    TokenExchangeRequest,
    AuthorizationRequest,
    UserProfile,
    normalize_claims,
)


def load_auth0_config() -> OAuthConfig:
    auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
    if not auth0_domain:
        raise ValueError("AUTH0_DOMAIN environment variable is required")

    domain = auth0_domain
    if not domain.startswith("http"):
        domain = f"https://{domain}"

    return OAuthConfig(
        provider="auth0",
        client_id=os.environ.get("AUTH0_CLIENT_ID", ""),
        client_secret=os.environ.get("AUTH0_CLIENT_SECRET", ""),
        redirect_uri=os.environ.get(
            "AUTH0_REDIRECT_URI", "http://localhost:3000/callback"
        ),
        authorization_endpoint=f"{domain}/authorize",
        token_endpoint=f"{domain}/oauth/token",
        userinfo_endpoint=f"{domain}/userinfo",
        scope=os.environ.get("AUTH0_SCOPE", "openid profile email"),
        audience=os.environ.get("AUTH0_AUDIENCE"),
        connection=os.environ.get("AUTH0_CONNECTION"),
    )


def load_pkce_config() -> PKCEConfig:
    return PKCEConfig()


def generate_pkce_pair() -> Tuple[str, str]:
    code_verifier = secrets.token_urlsafe(64)
    code_verifier_bytes = code_verifier.encode("ascii")
    sha256_hash = hashlib.sha256(code_verifier_bytes).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).rstrip(b"=").decode("ascii")
    return code_verifier, code_challenge


def build_authorization_url(
    config: OAuthConfig, pkce_config: Optional[PKCEConfig] = None
) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "response_type": config.response_type,
        "state": config.state,
        "nonce": config.nonce,
    }
    if pkce_config and pkce_config.code_challenge:
        params["code_challenge"] = pkce_config.code_challenge
        params["code_challenge_method"] = pkce_config.code_challenge_method
    if config.audience:
        params["audience"] = config.audience
    if config.connection:
        params["connection"] = config.connection

    query_string = "&".join(
        f"{k}={requests.utils.quote(str(v))}" for k, v in params.items()
    )
    return f"{config.authorization_endpoint}?{query_string}"


def exchange_code_for_tokens(
    config: OAuthConfig,
    code: str,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
        "client_secret": config.client_secret,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier

    response = requests.post(
        config.token_endpoint,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse(
        access_token=token_data["access_token"],
        token_type=token_data.get("token_type", "Bearer"),
        expires_in=token_data.get("expires_in", 3600),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        scope=token_data.get("scope"),
    )


def fetch_user_profile(config: OAuthConfig, access_token: str) -> UserProfile:
    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_claims(claims)


def validate_state(expected_state: str, received_state: str) -> bool:
    return secrets.compare_digest(expected_state, received_state)


def decode_id_token_claims(id_token: str) -> Dict[str, Any]:
    parts = id_token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT token format")
    payload = parts[1]
    padding = 4 - len(payload) % 4
    if padding != 4:
        payload += "=" * padding
    decoded = base64.urlsafe_b64decode(payload)
    return json.loads(decoded)


def create_http_session(
    base_url: str,
    api_key: Optional[str] = None,
    auth_header: str = "Authorization",
    auth_prefix: str = "Bearer",
    extra_headers: Optional[Dict[str, str]] = None,
) -> requests.Session:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    if api_key:
        session.headers[auth_header] = f"{auth_prefix} {api_key}"
    if extra_headers:
        session.headers.update(extra_headers)
    return session


def parse_callback_url(callback_url: str) -> Dict[str, str]:
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(callback_url)
    params = parse_qs(parsed.query)
    return {k: v[0] if len(v) == 1 else v for k, v in params.items()}
