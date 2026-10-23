import base64
import hashlib
import os
import secrets

import requests


def _code_challenge(verifier):
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("utf-8")


def pkce_login(payload, config=None):
    config = config or {}
    client_id = config["client_id"]
    redirect_uri = payload["redirect_uri"]
    verifier = payload.get("code_verifier") or secrets.token_urlsafe(64)
    state = payload.get("state") or secrets.token_urlsafe(32)
    authorization_url = "https://accounts.google.com/o/oauth2/v2/auth"
    query = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": payload.get("scope", "openid email profile"),
        "code_challenge": _code_challenge(verifier),
        "code_challenge_method": "S256",
        "state": state,
    }
    return {"authorization_url": authorization_url, "query": query, "code_verifier": verifier, "state": state}
