import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import load_config


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(redirect_uri: str) -> dict:
    config = load_config()
    verifier = secrets.token_urlsafe(64)
    params = {
        "client_id": config.auth0_client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "code_challenge": _challenge(verifier),
        "code_challenge_method": "S256",
    }
    return {
        "authorization_url": f"https://{config.auth0_domain}/authorize?{urlencode(params)}",
        "code_verifier": verifier,
    }
