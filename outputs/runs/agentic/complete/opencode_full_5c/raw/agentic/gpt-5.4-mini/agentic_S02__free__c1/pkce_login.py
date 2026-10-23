import base64
import hashlib
import secrets

from identity_client import build_authorization_url, load_identity_provider_config


def _code_verifier() -> str:
    return secrets.token_urlsafe(64)


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def pkce_login() -> dict:
    config = load_identity_provider_config("OIDC")
    verifier = _code_verifier()
    challenge = _code_challenge(verifier)
    state = secrets.token_urlsafe(32)
    authorization_url, returned_state = build_authorization_url(
        config, state, code_challenge=challenge
    )
    return {
        "authorization_url": authorization_url,
        "state": returned_state,
        "code_verifier": verifier,
    }
