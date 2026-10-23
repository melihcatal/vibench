from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import get_identity_settings
from identity_models import OAuthCallbackRequest, TokenSet, normalize_profile_claims

AUTH0_TOKEN_URL = "https://{domain}/oauth/token"
AUTH0_USERINFO_URL = "https://{domain}/userinfo"


def exchange_code_for_tokens(callback: OAuthCallbackRequest) -> TokenSet:
    settings = get_identity_settings()
    token_url = AUTH0_TOKEN_URL.format(domain=settings.auth0_domain)
    response = requests.post(
        token_url,
        json={
            "grant_type": "authorization_code",
            "client_id": settings.client_id,
            "client_secret": settings.client_secret,
            "code": callback.code,
            "redirect_uri": callback.redirect_uri or settings.redirect_uri,
            "code_verifier": callback.code_verifier,
        },
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    return TokenSet(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=int(payload.get("expires_in", 0) or 0),
        raw=payload,
    )


def fetch_userinfo(access_token: str) -> Dict[str, Any]:
    settings = get_identity_settings()
    userinfo_url = AUTH0_USERINFO_URL.format(domain=settings.auth0_domain)
    response = requests.get(
        userinfo_url,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def handle_oauth_callback(callback: OAuthCallbackRequest) -> Dict[str, Any]:
    tokens = exchange_code_for_tokens(callback)
    claims = fetch_userinfo(tokens.access_token)
    return normalize_profile_claims(claims, issuer="auth0") | {"tokens": tokens.to_dict()}
