from __future__ import annotations

from authlib.integrations.requests_client import OAuth2Session

from identity_client import load_identity_config


def pkce_login() -> dict:
    config = load_identity_config()
    session = OAuth2Session(client_id=config.client_id, scope=config.scope, redirect_uri=config.redirect_uri)
    code_verifier = session.create_code_verifier(48)
    code_challenge = session.create_code_challenge(code_verifier, method="S256")
    authorization_endpoint = f"{config.issuer_url.rstrip('/')}/authorize"
    uri, state = session.create_authorization_url(
        authorization_endpoint,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return {"authorization_url": uri, "state": state, "code_verifier": code_verifier}
