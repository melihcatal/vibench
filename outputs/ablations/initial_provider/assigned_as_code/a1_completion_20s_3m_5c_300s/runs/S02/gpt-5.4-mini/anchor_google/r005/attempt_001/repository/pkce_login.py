import base64
import hashlib
import os

import requests


def _pkce_verifier():
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("ascii")


def _pkce_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")


def pkce_login(payload, config=None):
    config = dict(config or {})
    verifier = payload.get("code_verifier") or _pkce_verifier()
    challenge = _pkce_challenge(verifier)
    request = {
        "providerId": config["provider_id"],
        "continueUri": payload["redirect_uri"],
        "codeChallengeMethod": "S256",
        "codeChallenge": challenge,
    }
    response = requests.post("https://identitytoolkit.googleapis.com/v1/accounts:createAuthUri",
                             params={"key": config["api_key"]}, json=request, timeout=30)
    response.raise_for_status()
    result = response.json()
    return {"authorization_url": result["authUri"], "session_id": result["sessionId"], "code_verifier": verifier}
