from __future__ import annotations

from identity_client import exchange_code_for_tokens, load_identity_config
from identity_models import TokenResponse


def handle_oauth_callback(code: str, code_verifier: str = "") -> TokenResponse:
    config = load_identity_config("AUTH0")
    return exchange_code_for_tokens(config, code=code, code_verifier=code_verifier)
