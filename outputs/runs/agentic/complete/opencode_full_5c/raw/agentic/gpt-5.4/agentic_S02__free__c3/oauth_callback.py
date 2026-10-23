from __future__ import annotations

from typing import Optional

from identity_client import exchange_code_for_tokens
from identity_models import CallbackRequest, TokenSet


def handle_oauth_callback(
    code: str,
    redirect_uri: str,
    state: Optional[str] = None,
    expected_state: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> dict:
    if expected_state is not None and state != expected_state:
        raise ValueError("State mismatch")
    callback = CallbackRequest(
        code=code,
        redirect_uri=redirect_uri,
        state=state,
        code_verifier=code_verifier,
    )
    payload = exchange_code_for_tokens(callback)
    return TokenSet.from_payload(payload, provider="auth0").to_dict()
