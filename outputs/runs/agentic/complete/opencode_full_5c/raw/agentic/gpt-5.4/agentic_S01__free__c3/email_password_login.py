from __future__ import annotations

from identity_client import (
    auth0_audience,
    auth0_client_id,
    auth0_client_secret,
    auth0_db_connection,
    auth0_post,
)
from identity_models import LoginRequest, normalize_auth0_tokens


def email_password_login(request: LoginRequest):
    payload = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "realm": auth0_db_connection(),
        "username": request.email,
        "password": request.password,
        "client_id": auth0_client_id(),
        "client_secret": auth0_client_secret(),
        "scope": request.scope,
    }
    audience = auth0_audience()
    if audience:
        payload["audience"] = audience
    response = auth0_post("/oauth/token", payload)
    return normalize_auth0_tokens(response)
