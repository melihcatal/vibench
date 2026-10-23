import os
import secrets
import urllib.parse
from identity_client import get_oauth_config


def start_oauth_login(redirect_uri, state=None, nonce=None):
    config = get_oauth_config()

    if state is None:
        state = secrets.token_urlsafe(16)
    if nonce is None:
        nonce = secrets.token_urlsafe(16)

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = code_verifier

    params = {
        "client_id": config["client_id"],
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "plain",
    }

    auth_url = f"https://{config['domain']}/authorize"
    query_string = urllib.parse.urlencode(params)
    full_url = f"{auth_url}?{query_string}"

    return {
        "auth_url": full_url,
        "state": state,
        "nonce": nonce,
        "code_verifier": code_verifier,
    }
