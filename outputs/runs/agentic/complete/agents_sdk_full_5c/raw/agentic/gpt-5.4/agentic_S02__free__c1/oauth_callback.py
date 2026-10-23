from __future__ import annotations

from identity_client import load_auth0_settings, post_token
from identity_models import TokenExchangeRequest, TokenSet, normalize_scopes


def exchange_oauth_callback(request: TokenExchangeRequest) -> TokenSet:
    settings = load_auth0_settings()
    payload = {
        "grant_type": "authorization_code",
        "client_id": settings.client_id,
        "code": request.code,
        "redirect_uri": request.redirect_uri,
    }
    if settings.client_secret:
        payload["client_secret"] = settings.client_secret
    if request.code_verifier:
        payload["code_verifier"] = request.code_verifier
    raw = post_token(payload)
    return TokenSet(
        access_token=str(raw["access_token"]),
        id_token=raw.get("id_token"),
        refresh_token=raw.get("refresh_token"),
        token_type=str(raw.get("token_type", "Bearer")),
        expires_in=raw.get("expires_in"),
        scope=normalize_scopes(raw.get("scope")),
        raw=raw,
    )
