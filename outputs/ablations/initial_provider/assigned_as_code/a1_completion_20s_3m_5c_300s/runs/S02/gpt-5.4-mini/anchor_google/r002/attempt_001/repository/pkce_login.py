import base64
import hashlib
import secrets

import requests

from identity_client import load_identity_config


def _challenge(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(payload, config=None):
    config = load_identity_config(config)
    verifier = payload.get("code_verifier") or secrets.token_urlsafe(64)
    challenge = _challenge(verifier)
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    query = {
        "response_type": "code",
        "client_id": config.google_client_id,
        "redirect_uri": payload["redirect_uri"],
        "scope": "openid email profile",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent",
    }
    return {"authorization_url": requests.Request("GET", auth_url, params=query).prepare().url, "code_verifier": verifier}
