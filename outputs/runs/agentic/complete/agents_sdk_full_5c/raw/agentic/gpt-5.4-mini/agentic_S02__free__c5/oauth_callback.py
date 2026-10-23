from __future__ import annotations

from authlib.integrations.requests_client import OAuth2Session

from identity_client import load_identity_config
from identity_models import TokenResponse


def oauth_callback(code: str, state: str) -> TokenResponse:
    config = load_identity_config()
    session = OAuth2Session(client_id=config.client_id, client_secret=config.client_secret, state=state, redirect_uri=config.redirect_uri)
    token_endpoint = f"{config.issuer_url.rstrip('/')}/token"
    token = session.fetch_token(token_endpoint, code=code, grant_type="authorization_code")
    return TokenResponse(
        access_token=token["access_token"],
        id_token=token.get("id_token"),
        refresh_token=token.get("refresh_token"),
        token_type=token.get("token_type", "Bearer"),
        expires_in=token.get("expires_in"),
    )
