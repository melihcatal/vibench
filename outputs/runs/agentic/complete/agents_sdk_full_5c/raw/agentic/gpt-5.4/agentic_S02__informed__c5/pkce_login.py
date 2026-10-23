from __future__ import annotations

from typing import Dict, Optional

from identity_client import (
    build_authorization_url,
    generate_pkce_challenge,
    generate_pkce_verifier,
    load_auth0_settings,
)


PROVIDER = "Auth0 Authentication API"



def start_pkce_login(
    redirect_uri: str,
    state: str,
    scopes: Optional[list[str]] = None,
    audience: Optional[str] = None,
) -> Dict[str, str]:
    settings = load_auth0_settings()
    verifier = generate_pkce_verifier()
    challenge = generate_pkce_challenge(verifier)
    authorization_url = build_authorization_url(
        settings=settings,
        redirect_uri=redirect_uri,
        state=state,
        scope=" ".join(scopes or ["openid", "profile", "email"]),
        audience=audience,
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    return {
        "provider": PROVIDER,
        "authorization_url": authorization_url,
        "code_verifier": verifier,
        "code_challenge_method": "S256",
    }
