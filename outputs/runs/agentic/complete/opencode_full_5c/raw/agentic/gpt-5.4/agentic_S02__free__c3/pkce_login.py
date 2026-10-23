from __future__ import annotations

from typing import Iterable, Optional

from identity_client import (
    build_authorization_url,
    build_code_challenge,
    ensure_scopes,
    generate_code_verifier,
    generate_nonce,
    generate_state,
)
from identity_models import PKCELoginRequest


def start_pkce_login(
    redirect_uri: str,
    scopes: Optional[Iterable[str]] = None,
    prompt: Optional[str] = None,
    login_hint: Optional[str] = None,
) -> dict:
    state = generate_state()
    nonce = generate_nonce()
    code_verifier = generate_code_verifier()
    code_challenge = build_code_challenge(code_verifier)
    request = PKCELoginRequest(
        state=state,
        redirect_uri=redirect_uri,
        scopes=ensure_scopes(scopes),
        prompt=prompt,
        login_hint=login_hint,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    authorization_url = build_authorization_url(request, use_pkce=True)
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }
