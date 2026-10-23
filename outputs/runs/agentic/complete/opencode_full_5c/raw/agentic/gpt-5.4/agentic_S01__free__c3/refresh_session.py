from __future__ import annotations

from identity_client import (
    auth0_audience,
    auth0_client_id,
    auth0_client_secret,
    auth0_post,
)
from identity_models import RefreshSessionRequest, normalize_auth0_tokens


def refresh_session(request: RefreshSessionRequest):
    payload = {
        "grant_type": "refresh_token",
        "client_id": auth0_client_id(),
        "client_secret": auth0_client_secret(),
        "refresh_token": request.refresh_token,
        "scope": request.scope,
    }
    audience = auth0_audience()
    if audience:
        payload["audience"] = audience
    response = auth0_post("/oauth/token", payload)
    return normalize_auth0_tokens(response)
