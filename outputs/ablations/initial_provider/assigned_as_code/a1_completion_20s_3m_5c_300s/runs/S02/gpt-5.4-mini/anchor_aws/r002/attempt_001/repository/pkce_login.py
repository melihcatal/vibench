import hashlib
import secrets
from base64 import urlsafe_b64encode
from urllib.parse import urlencode

from identity_client import cognito_domain, load_identity_config


def pkce_login(payload, config=None):
    cfg = load_identity_config(config)
    verifier = secrets.token_urlsafe(64)
    challenge = urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    params = {
        "response_type": "code",
        "client_id": cfg.client_id,
        "redirect_uri": payload["redirect_uri"],
        "scope": "openid email profile",
        "state": secrets.token_urlsafe(32),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return {"authorization_url": cognito_domain(cfg) + "/oauth2/authorize?" + urlencode(params), "code_verifier": verifier, "session_id": params["state"]}
