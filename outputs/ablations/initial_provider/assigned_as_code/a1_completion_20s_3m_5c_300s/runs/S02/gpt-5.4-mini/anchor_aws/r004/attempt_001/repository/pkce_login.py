import hashlib
import secrets
from base64 import urlsafe_b64encode
from urllib.parse import urlencode


def _code_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode()).digest()
    return urlsafe_b64encode(digest).rstrip(b"=").decode()


def pkce_login(payload, config=None):
    config = config or {}
    verifier = secrets.token_urlsafe(64)
    challenge = _code_challenge(verifier)
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    query = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": payload["redirect_uri"],
        "scope": "openid email profile",
        "state": secrets.token_urlsafe(32),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return {"authorization_url": domain + "/oauth2/authorize?" + urlencode(query), "code_verifier": verifier}
