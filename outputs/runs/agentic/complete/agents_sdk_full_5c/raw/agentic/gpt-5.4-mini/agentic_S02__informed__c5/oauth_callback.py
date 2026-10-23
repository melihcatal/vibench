from __future__ import annotations

from typing import Dict

from identity_client import exchange_code_for_tokens


def handle_callback(code: str, redirect_uri: str, code_verifier: str) -> Dict[str, object]:
    tokens = exchange_code_for_tokens(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)
    return {
        "access_token": tokens.access_token,
        "id_token": tokens.id_token,
        "refresh_token": tokens.refresh_token,
        "token_type": tokens.token_type,
        "expires_in": tokens.expires_in,
        "raw": tokens.raw,
    }
