from __future__ import annotations

from identity_client import auth0_client_id, auth0_client_secret, auth0_post
from identity_models import (
    RefreshSessionRequest,
    TokenResponse,
    normalize_token_response,
)


def refresh_session(request: RefreshSessionRequest) -> TokenResponse:
    response = auth0_post(
        "/oauth/token",
        request.to_auth0_payload(auth0_client_id(), auth0_client_secret()),
    )
    return normalize_token_response(response)
