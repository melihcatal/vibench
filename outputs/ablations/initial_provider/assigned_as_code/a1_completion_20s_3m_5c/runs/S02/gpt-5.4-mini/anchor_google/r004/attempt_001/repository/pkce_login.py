import hashlib
import base64
import secrets

import requests

from identity_client import load_identity_config


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def pkce_login(payload, config=None):
    config = load_identity_config(config)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = _b64url(hashlib.sha256(code_verifier.encode("ascii")).digest())
    params = {
        "client_id": config["client_id"],
        "redirect_uri": payload["redirect_uri"],
        "response_type": "code",
        "scope": payload.get("scope", "openid email profile"),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    response = requests.Request("GET", "https://accounts.google.com/o/oauth2/v2/auth", params=params).prepare()
    return {"authorization_url": response.url, "code_verifier": code_verifier}
