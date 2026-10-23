import base64
import hashlib
import secrets
import urllib.parse

from identity_client import load_identity_config


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return base64.urlsafe_b64encode(digest).decode().rstrip("=")


def create_pkce_login_url(state: str, nonce: str | None = None):
    cfg = load_identity_config()
    verifier = secrets.token_urlsafe(64)
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": cfg.redirect_uri,
        "scope": cfg.scope,
        "state": state,
        "code_challenge": _challenge(verifier),
        "code_challenge_method": "S256",
    }
    if nonce:
        params["nonce"] = nonce
    return f"{cfg.authorize_url}?{urllib.parse.urlencode(params)}", verifier
