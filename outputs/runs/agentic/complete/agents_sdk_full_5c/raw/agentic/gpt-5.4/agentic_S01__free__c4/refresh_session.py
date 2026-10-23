from __future__ import annotations

from identity_client import post_form, secure_token_url
from identity_models import AuthTokens, RefreshSessionRequest, parse_refresh_response



def refresh_session(refresh_token: str) -> AuthTokens:
    request_model = RefreshSessionRequest(refresh_token=refresh_token)
    response_data = post_form(secure_token_url(), request_model.to_securetoken_payload())
    return parse_refresh_response(response_data)
