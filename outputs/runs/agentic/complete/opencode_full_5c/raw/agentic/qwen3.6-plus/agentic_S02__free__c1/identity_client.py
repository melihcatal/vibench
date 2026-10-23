import os
import json
import base64
import hashlib
import secrets
from typing import Optional, Dict, Any
from urllib.parse import urlencode

from identity_models import OAuthConfig, TokenResponse


def load_config_from_env(provider: str) -> OAuthConfig:
    provider_upper = provider.upper()
    return OAuthConfig(
        provider=provider,
        client_id=os.environ.get(f"{provider_upper}_CLIENT_ID", ""),
        client_secret=os.environ.get(f"{provider_upper}_CLIENT_SECRET"),
        redirect_uri=os.environ.get(
            f"{provider_upper}_REDIRECT_URI", "http://localhost:3000/callback"
        ),
        authorize_url=os.environ.get(f"{provider_upper}_AUTHORIZE_URL", ""),
        token_url=os.environ.get(f"{provider_upper}_TOKEN_URL", ""),
        userinfo_url=os.environ.get(f"{provider_upper}_USERINFO_URL", ""),
        scopes=json.loads(
            os.environ.get(f"{provider_upper}_SCOPES", '["openid", "profile", "email"]')
        ),
        extra_params=json.loads(os.environ.get(f"{provider_upper}_EXTRA_PARAMS", "{}")),
    )


def load_config_from_file(path: str, provider: str) -> OAuthConfig:
    with open(path, "r") as f:
        data = json.load(f)
    provider_data = data.get(provider, data)
    return OAuthConfig(
        provider=provider,
        client_id=provider_data["client_id"],
        client_secret=provider_data.get("client_secret"),
        redirect_uri=provider_data.get(
            "redirect_uri", "http://localhost:3000/callback"
        ),
        authorize_url=provider_data.get("authorize_url", ""),
        token_url=provider_data.get("token_url", ""),
        userinfo_url=provider_data.get("userinfo_url", ""),
        scopes=provider_data.get("scopes", ["openid", "profile", "email"]),
        extra_params=provider_data.get("extra_params", {}),
    )


def build_authorization_url(
    config: OAuthConfig,
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
    code_challenge_method: str = "S256",
) -> str:
    params = {
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "response_type": "code",
        "scope": " ".join(config.scopes),
    }
    if state:
        config.state = state
        params["state"] = state
    if nonce:
        config.nonce = nonce
        params["nonce"] = nonce
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method
    params.update(config.extra_params)
    query = urlencode(params)
    return f"{config.authorize_url}?{query}"


def generate_pkce_pair() -> tuple[str, str]:
    code_verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )
    return code_verifier, code_challenge


def exchange_authorization_code(
    config: OAuthConfig,
    code: str,
    code_verifier: Optional[str] = None,
) -> TokenResponse:
    import requests

    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.redirect_uri,
        "client_id": config.client_id,
    }
    if config.client_secret:
        body["client_secret"] = config.client_secret
    if code_verifier:
        body["code_verifier"] = code_verifier

    response = requests.post(config.token_url, data=body, timeout=30)
    response.raise_for_status()
    data = response.json()

    return TokenResponse(
        access_token=data["access_token"],
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 3600),
        refresh_token=data.get("refresh_token"),
        id_token=data.get("id_token"),
        scope=data.get("scope"),
        raw_response=data,
    )


def fetch_userinfo(config: OAuthConfig, access_token: str) -> Dict[str, Any]:
    import requests

    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(config.userinfo_url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def validate_id_token(
    id_token: str, expected_nonce: Optional[str] = None
) -> Dict[str, Any]:
    import jwt

    payload = jwt.decode(id_token, options={"verify_signature": False})
    if expected_nonce and payload.get("nonce") != expected_nonce:
        raise ValueError("Nonce mismatch in ID token")
    return payload
