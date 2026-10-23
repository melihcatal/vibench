from __future__ import annotations

from authlib.integrations.requests_client import OAuth2Session

from identity_client import load_identity_config
from identity_models import LoginRequest


def start_oauth_login() -> dict:
    config = load_identity_config()
    session = OAuth2Session(client_id=config.client_id, scope=config.scope, redirect_uri=config.redirect_uri)
    authorization_endpoint = f"{config.issuer_url.rstrip('/')}/authorize"
    uri, state = session.create_authorization_url(authorization_endpoint)
    request = LoginRequest(provider=config.issuer_url, redirect_uri=config.redirect_uri or "", scope=config.scope)
    return {"login_request": request.__dict__, "authorization_url": uri, "state": state}
