import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import get_cognito_base_url, get_oauth_config


def _code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def pkce_login(payload, config=None):
    cfg = get_oauth_config(config)
    verifier = secrets.token_urlsafe(64)
    state = secrets.token_urlsafe(32)
    query = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": payload["redirect_uri"],
        "scope": payload.get("scope", "openid email profile"),
        "state": state,
        "code_challenge": _code_challenge(verifier),
        "code_challenge_method": "S256",
    }
    if cfg.identity_provider:
        query["identity_provider"] = cfg.identity_provider
    return {
        "authorization_url": get_cognito_base_url(cfg) + "/oauth2/authorize?" + urlencode(query),
        "session_id": state,
        "code_verifier": verifier,
    }
