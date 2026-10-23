from __future__ import annotations

from identity_client import AUTH0_CLIENT_ID, AUTH0_DOMAIN, AUTH0_REDIRECT_URI, build_auth0_authorize_url, pkce_pair
from identity_models import LoginRequest


def pkce_login() -> dict[str, str]:
    verifier, challenge = pkce_pair()
    request = LoginRequest(
        issuer=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        code_verifier=verifier,
        code_challenge=challenge,
    )
    return {
        "authorization_url": build_auth0_authorize_url(request),
        "code_verifier": verifier,
        "code_challenge": challenge,
    }
