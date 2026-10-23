import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode

from identity_client import get_auth0_config

def generate_pkce_challenge() -> (str, str):
    code_verifier = secrets.token_urlsafe(64)
    # S256 code_challenge method
    s256_hash = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256_hash).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge


def start_pkce_login(redirect_uri: str, scope: str = "openid profile email") -> dict:
    config = get_auth0_config()
    domain = config["AUTH0_DOMAIN"]
    client_id = config["AUTH0_CLIENT_ID"]

    code_verifier, code_challenge = generate_pkce_challenge()

    authorize_url = f"https://{domain}/authorize"
    params = {
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "audience": config["AUTH0_API_AUDIENCE"], # Optional, if API access is needed
    }
    
    # Store code_verifier in a session for later use in the token exchange
    # In a real application, this would be stored in a secure session store
    # For this example, we just return it.
    return {
        "authorization_url": f"{authorize_url}?{urlencode(params)}",
        "code_verifier": code_verifier
    }
