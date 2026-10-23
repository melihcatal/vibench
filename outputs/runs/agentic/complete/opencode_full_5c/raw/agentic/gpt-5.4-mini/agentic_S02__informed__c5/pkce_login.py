import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import authorization_endpoint, load_identity_config


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def build_pkce_login_url(redirect_uri: str | None = None) -> tuple[str, str, str]:
    config = load_identity_config("AUTH0")
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = _challenge(code_verifier)
    state = secrets.token_urlsafe(24)
    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri or config.redirect_uri or "",
        "scope": config.scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return (
        f"{authorization_endpoint(config)}?{urlencode({k: v for k, v in params.items() if v})}",
        state,
        code_verifier,
    )
