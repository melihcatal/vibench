import os
import secrets
import hashlib
import base64
import urllib.parse
from identity_client import get_oauth_config


def generate_pkce_pair():
    code_verifier = secrets.token_urlsafe(64)

    code_challenge_bytes = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge_bytes).decode().replace("=", "")
    )

    return {"code_verifier": code_verifier, "code_challenge": code_challenge}


def start_pkce_login(redirect_uri, state=None, nonce=None):
    config = get_oauth_config()

    if state is None:
        state = secrets.token_urlsafe(16)
    if nonce is None:
        nonce = secrets.token_urlsafe(16)

    pkce_pair = generate_pkce_pair()

    params = {
        "client_id": config["client_id"],
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
        "code_challenge": pkce_pair["code_challenge"],
        "code_challenge_method": "S256",
    }

    auth_url = f"https://{config['domain']}/authorize"
    query_string = urllib.parse.urlencode(params)
    full_url = f"{auth_url}?{query_string}"

    return {
        "auth_url": full_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": pkce_pair["code_verifier"],
    }
