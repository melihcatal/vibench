import os
import json
import base64
import hashlib
import secrets
import requests
from typing import Optional
from urllib.parse import urlencode

from identity_models import (
    OAuthConfig,
    TokenResponse,
    UserProfile,
    PKCEChallenge,
    normalize_claims,
)


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", "")
DEFAULT_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI", "http://localhost:3000/callback")
DEFAULT_SCOPE = os.getenv("AUTH0_SCOPE", "openid profile email")


def load_oauth_config(
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
) -> OAuthConfig:
    return OAuthConfig(
        provider="auth0",
        domain=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        redirect_uri=redirect_uri or DEFAULT_REDIRECT_URI,
        audience=audience or AUTH0_AUDIENCE,
        scope=scope or DEFAULT_SCOPE,
        state=state or secrets.token_urlsafe(32),
        nonce=nonce or secrets.token_urlsafe(32),
    )


def build_auth_url(
    config: OAuthConfig,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = "S256",
    connection: Optional[str] = None,
    prompt: Optional[str] = None,
    max_age: Optional[int] = None,
    extra_params: Optional[dict] = None,
) -> str:
    params = {
        "response_type": config.response_type,
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "scope": config.scope,
        "state": config.state,
        "nonce": config.nonce,
    }
    if config.audience:
        params["audience"] = config.audience
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method
    if connection:
        params["connection"] = connection
    if prompt:
        params["prompt"] = prompt
    if max_age is not None:
        params["max_age"] = str(max_age)
    if extra_params:
        params.update(extra_params)
    query = urlencode(params)
    return f"{config.authorize_url}?{query}"


def exchange_code_for_tokens(
    config: OAuthConfig,
    authorization_code: str,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    token_payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
    }
    if code_verifier:
        token_payload["code_verifier"] = code_verifier

    response = requests.post(
        config.token_url,
        json=token_payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    return TokenResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        refresh_token=data.get("refresh_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 0),
        scope=data.get("scope", config.scope),
    )


def fetch_user_info(
    config: OAuthConfig,
    access_token: str,
) -> UserProfile:
    response = requests.get(
        config.userinfo_url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()
    return normalize_claims(claims, provider="auth0")


def verify_id_token_signature(
    id_token: str,
    domain: str,
) -> bool:
    parts = id_token.split(".")
    if len(parts) != 3:
        return False
    try:
        payload_bytes = base64.urlsafe_b64decode(parts[1] + "==")
        payload = json.loads(payload_bytes)
        expected_issuer = f"https://{domain}/"
        return payload.get("iss") == expected_issuer
    except Exception:
        return False


def revoke_token(
    config: OAuthConfig,
    token: str,
    token_type_hint: str = "access_token",
) -> bool:
    response = requests.post(
        f"https://{config.domain}/oauth/revoke",
        json={
            "client_id": config.client_id,
            "client_secret": config.client_secret,
            "token": token,
            "token_type_hint": token_type_hint,
        },
        headers={"Content-Type": "application/json"},
        timeout=30,
    )
    return response.status_code == 200


def generate_pkce_pair() -> PKCEChallenge:
    return PKCEChallenge.generate()


def create_auth0_session(
    config: OAuthConfig,
    token_response: TokenResponse,
    user_profile: UserProfile,
) -> dict:
    return {
        "access_token": token_response.access_token,
        "id_token": token_response.id_token,
        "refresh_token": token_response.refresh_token,
        "token_type": token_response.token_type,
        "expires_in": token_response.expires_in,
        "user": user_profile.to_dict(),
        "provider": "auth0",
        "domain": config.domain,
    }
