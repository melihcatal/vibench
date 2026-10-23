from __future__ import annotations

from identity_client import AUTH0_REDIRECT_URI, exchange_code_for_tokens, load_callback_payload
from identity_models import TokenResponse


def handle_oauth_callback(payload: dict | str | bytes) -> TokenResponse:
    data = load_callback_payload(payload)
    code = str(data.get("code", ""))
    if not code:
        raise ValueError("missing authorization code")
    code_verifier = data.get("code_verifier")
    return exchange_code_for_tokens(code=code, redirect_uri=AUTH0_REDIRECT_URI, code_verifier=code_verifier)
