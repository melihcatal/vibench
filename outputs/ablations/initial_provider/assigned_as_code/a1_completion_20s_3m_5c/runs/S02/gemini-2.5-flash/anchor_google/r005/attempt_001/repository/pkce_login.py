import os
import secrets
import hashlib
import base64
from identity_client import get_provider_config

def start_pkce_login(redirect_uri: str) -> dict:
    provider_config = get_provider_config()
    authorization_endpoint = provider_config.get("authorization_endpoint")
    client_id = os.environ.get("OAUTH_CLIENT_ID")

    if not authorization_endpoint or not client_id:
        raise ValueError("OAUTH_AUTHORIZATION_ENDPOINT and OAUTH_CLIENT_ID must be set")

    code_verifier = secrets.token_urlsafe(64)
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email", # Example scopes
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    from urllib.parse import urlencode
    authorization_url = f"{authorization_endpoint}?{urlencode(params)}"

    return {"authorization_url": authorization_url, "code_verifier": code_verifier}
