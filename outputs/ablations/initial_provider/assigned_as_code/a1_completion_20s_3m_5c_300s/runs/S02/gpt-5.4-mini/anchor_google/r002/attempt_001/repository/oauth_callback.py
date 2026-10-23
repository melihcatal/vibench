import base64
import hashlib

import requests

from identity_client import load_identity_config


def oauth_callback(payload, config=None):
    config = load_identity_config(config)
    token_request = {
        "grant_type": "authorization_code",
        "code": payload["code"],
        "redirect_uri": payload["redirect_uri"],
        "client_id": config.google_client_id or config.provider_id,
    }
    if config.google_client_secret:
        token_request["client_secret"] = config.google_client_secret
    response = requests.post("https://oauth2.googleapis.com/token", data=token_request, timeout=30)
    response.raise_for_status()
    tokens = response.json()
    userinfo = requests.get("https://openidconnect.googleapis.com/v1/userinfo", headers={"Authorization": f"Bearer {tokens['access_token']}"}, timeout=30)
    userinfo.raise_for_status()
    profile = userinfo.json()
    return {"tokens": tokens, "claims": profile}
