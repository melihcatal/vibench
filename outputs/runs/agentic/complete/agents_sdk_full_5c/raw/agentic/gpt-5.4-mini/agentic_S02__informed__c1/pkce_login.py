from __future__ import annotations

import base64
import hashlib
import secrets

from identity_client import build_authorize_url, load_identity_config
from identity_models import LoginRequest


def _code_verifier() -> str:
    return secrets.token_urlsafe(64)


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def start_pkce_login(state: str, nonce: str, redirect_uri: str = "") -> tuple[str, str]:
    config = load_identity_config("AUTH0")
    verifier = _code_verifier()
    challenge = _code_challenge(verifier)
    req = LoginRequest(redirect_uri=redirect_uri or config.redirect_uri, state=state, nonce=nonce)
    return build_authorize_url(config, req, code_challenge=challenge, code_challenge_method="S256"), verifier
