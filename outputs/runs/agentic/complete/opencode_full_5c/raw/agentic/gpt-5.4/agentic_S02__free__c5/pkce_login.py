from __future__ import annotations

from identity_client import (
    build_authorize_url,
    generate_code_challenge,
    generate_code_verifier,
)
from identity_models import PKCELoginRequest


def pkce_login(request: PKCELoginRequest | None = None) -> dict[str, str]:
    if request is None:
        verifier = generate_code_verifier()
        request = PKCELoginRequest(
            state=verifier[:24], redirect_uri="", code_verifier=verifier
        )
    code_challenge = generate_code_challenge(request.code_verifier)
    authorization_url = build_authorize_url(
        redirect_uri=request.redirect_uri,
        state=request.state,
        scope=request.scope,
        prompt=request.prompt,
        audience=request.audience,
        code_challenge=code_challenge,
    )
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "state": request.state,
        "code_verifier": request.code_verifier,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
