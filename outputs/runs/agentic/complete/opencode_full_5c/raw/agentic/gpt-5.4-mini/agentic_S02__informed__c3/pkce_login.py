import base64
import hashlib
import secrets

from identity_client import Auth0Config, auth0_authorize_url


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def pkce_login(redirect_uri: str, state: str) -> dict:
    verifier = secrets.token_urlsafe(64)
    challenge = _challenge(verifier)
    cfg = Auth0Config()
    return {
        "authorization_url": auth0_authorize_url(
            cfg, redirect_uri=redirect_uri, state=state, code_challenge=challenge
        ),
        "code_verifier": verifier,
        "code_challenge": challenge,
    }
