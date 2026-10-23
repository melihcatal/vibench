import secrets
import hashlib
import base64
from urllib.parse import urlencode
import os

def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def pkce_login(payload, config=None):
    config = config or {}
    code_verifier, code_challenge = generate_pkce_challenge()
    state = secrets.token_urlsafe(32)

    domain = f"https://{config.get('domain_prefix', os.environ.get('COGNITO_DOMAIN_PREFIX'))}.auth.{config.get('region', os.environ.get('COGNITO_REGION'))}.amazoncognito.com"
    query = {
        "response_type": "code",
        "client_id": config.get("client_id", os.environ.get("COGNITO_CLIENT_ID")),
        "redirect_uri": payload["redirect_uri"],
        "scope": "openid email profile",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    if config.get("identity_provider"):
        query["identity_provider"] = config["identity_provider"]

    return {
        "authorization_url": domain + "/oauth2/authorize?" + urlencode(query),
        "session_id": state,
        "code_verifier": code_verifier
    }
