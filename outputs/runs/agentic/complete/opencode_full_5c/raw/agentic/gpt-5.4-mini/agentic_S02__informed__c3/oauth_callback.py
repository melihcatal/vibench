import os

from identity_client import Auth0Config, auth0_token_endpoint, post_form
from identity_models import OAuthTokenResponse


def oauth_callback(
    code: str, redirect_uri: str, code_verifier: str = ""
) -> OAuthTokenResponse:
    cfg = Auth0Config()
    payload = {
        "grant_type": "authorization_code",
        "client_id": cfg.client_id,
        "client_secret": cfg.client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    tokens = post_form(auth0_token_endpoint(cfg), payload)
    return OAuthTokenResponse(
        access_token=tokens.get("access_token", ""),
        id_token=tokens.get("id_token", ""),
        refresh_token=tokens.get("refresh_token", ""),
        token_type=tokens.get("token_type", "Bearer"),
        expires_in=int(tokens.get("expires_in", 0)),
    )
