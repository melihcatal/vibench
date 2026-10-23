from __future__ import annotations

from identity_client import firebase_refresh_token
from identity_models import RefreshRequest, normalize_token_response


def refresh_session(request: RefreshRequest):
    response = firebase_refresh_token(request.refresh_token)
    return normalize_token_response(response)
