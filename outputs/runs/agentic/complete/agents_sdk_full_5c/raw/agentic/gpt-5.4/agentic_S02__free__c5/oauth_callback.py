from __future__ import annotations

from typing import Mapping, Optional

from identity_client import Auth0Client
from identity_models import CallbackResult, OAuthState, normalize_scopes


class OAuthCallbackError(ValueError):
    pass


def handle_oauth_callback(params: Mapping[str, str], expected_state: OAuthState) -> CallbackResult:
    if params.get("error"):
        raise OAuthCallbackError(params.get("error_description") or params["error"])

    returned_state = params.get("state")
    if not returned_state or returned_state != expected_state.value:
        raise OAuthCallbackError("State mismatch during Auth0 callback processing")

    code: Optional[str] = params.get("code")
    if not code:
        raise OAuthCallbackError("Missing authorization code from Auth0 callback")

    client = Auth0Client()
    token_payload = client.exchange_code(code, code_verifier=expected_state.code_verifier)
    return CallbackResult(
        access_token=token_payload["access_token"],
        id_token=token_payload.get("id_token"),
        refresh_token=token_payload.get("refresh_token"),
        token_type=token_payload.get("token_type", "Bearer"),
        expires_in=token_payload.get("expires_in"),
        scope=normalize_scopes(token_payload.get("scope")),
        raw=token_payload,
    )
