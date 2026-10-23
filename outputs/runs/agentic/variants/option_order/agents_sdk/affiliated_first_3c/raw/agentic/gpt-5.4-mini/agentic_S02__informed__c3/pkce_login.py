from __future__ import annotations

from identity_client import auth0_authorize_url, load_auth0_config, make_pkce_pair
from identity_models import AuthorizationRequest


def build_pkce_login_url(state: str, nonce: str) -> tuple[str, str]:
    cfg = load_auth0_config()
    verifier, challenge = make_pkce_pair()
    req = AuthorizationRequest(
        issuer=cfg["issuer"],
        client_id=cfg["client_id"],
        redirect_uri=cfg["redirect_uri"],
        state=state,
        nonce=nonce,
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    return auth0_authorize_url(req), verifier
