from __future__ import annotations

import base64
import hashlib
import secrets
from typing import Dict

from identity_client import Auth0Client, load_auth0_config, new_nonce, new_state_token
from identity_models import OAuthState, TokenBundle


_pkce_store: Dict[str, OAuthState] = {}


def _generate_code_verifier() -> str:
    return secrets.token_urlsafe(64)


def _generate_code_challenge(code_verifier: str) -> str:
    digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def start_pkce_login() -> dict:
    config = load_auth0_config(public_client=True)
    client = Auth0Client(config)
    state = new_state_token()
    nonce = new_nonce()
    code_verifier = _generate_code_verifier()
    code_challenge = _generate_code_challenge(code_verifier)
    _pkce_store[state] = OAuthState(
        state=state,
        nonce=nonce,
        code_verifier=code_verifier,
        redirect_uri=config.redirect_uri,
    )
    authorization_url = client.build_authorization_url(
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "state": state,
        "code_challenge_method": "S256",
    }


def finish_pkce_login(code: str, state: str) -> TokenBundle:
    saved = _pkce_store.get(state)
    if not saved or not saved.code_verifier:
        raise ValueError("Unknown or expired PKCE state")
    client = Auth0Client(load_auth0_config(public_client=True))
    token_response = client.exchange_code(code=code, code_verifier=saved.code_verifier)
    return TokenBundle(
        access_token=token_response["access_token"],
        token_type=token_response.get("token_type", "Bearer"),
        expires_in=token_response.get("expires_in"),
        refresh_token=token_response.get("refresh_token"),
        id_token=token_response.get("id_token"),
        scope=token_response.get("scope"),
        provider="auth0",
    )
