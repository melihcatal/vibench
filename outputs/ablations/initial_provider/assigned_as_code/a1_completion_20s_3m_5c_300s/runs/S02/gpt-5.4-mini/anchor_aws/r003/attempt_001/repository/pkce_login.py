import hashlib
import base64
import secrets

from identity_client import cognito_authorize_url, load_identity_config


def _challenge(verifier):
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(payload, config=None):
    config = load_identity_config(config)
    verifier = secrets.token_urlsafe(64)
    state = secrets.token_urlsafe(32)
    url = cognito_authorize_url(config, payload["redirect_uri"], state, scopes=payload.get("scopes"), code_challenge=_challenge(verifier))
    return {"authorization_url": url, "state": state, "code_verifier": verifier}
