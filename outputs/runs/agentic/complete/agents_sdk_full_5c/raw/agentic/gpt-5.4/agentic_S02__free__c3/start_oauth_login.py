from __future__ import annotations

from typing import Dict

from identity_client import Auth0Client, load_auth0_config, new_nonce, new_state_token
from identity_models import OAuthState


_state_store: Dict[str, OAuthState] = {}


def start_oauth_login(prompt: str | None = None) -> dict:
    config = load_auth0_config(public_client=False)
    client = Auth0Client(config)
    state = new_state_token()
    nonce = new_nonce()
    _state_store[state] = OAuthState(state=state, nonce=nonce, redirect_uri=config.redirect_uri)
    authorization_url = client.build_authorization_url(state=state, nonce=nonce, prompt=prompt)
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "state": state,
        "redirect_uri": config.redirect_uri,
    }


def get_saved_state(state: str) -> OAuthState | None:
    return _state_store.get(state)
