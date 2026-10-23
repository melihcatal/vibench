import base64
import hashlib
import secrets
from urllib.parse import urlencode


def _verifier():
    return secrets.token_urlsafe(64)


def _challenge(verifier):
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(payload, config=None):
    config = config or {}
    verifier = _verifier()
    challenge = _challenge(verifier)
    domain = f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com"
    query = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": payload["redirect_uri"],
        "scope": payload.get("scope", "openid email profile"),
        "state": secrets.token_urlsafe(32),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if config.get("identity_provider"):
        query["identity_provider"] = config["identity_provider"]
    return {"authorization_url": domain + "/oauth2/authorize?" + urlencode(query), "code_verifier": verifier, "session_id": query["state"]}
