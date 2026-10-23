from __future__ import annotations

from identity_client import (
    build_authorization_url,
    generate_pkce_challenge,
    generate_pkce_verifier,
    load_okta_config,
)
from identity_models import PKCELoginRequest


def pkce_login(request: PKCELoginRequest | None = None) -> dict[str, str]:
    config = load_okta_config()
    code_verifier = generate_pkce_verifier()
    code_challenge = generate_pkce_challenge(code_verifier)
    prepared = request or PKCELoginRequest(
        state="", redirect_uri="", code_challenge=code_challenge
    )
    prepared.code_challenge = code_challenge
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        **prepared.to_params(),
    }
    authorization_url = build_authorization_url(config.authorization_endpoint, params)
    return {
        "provider": "okta",
        "authorization_url": authorization_url,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }
