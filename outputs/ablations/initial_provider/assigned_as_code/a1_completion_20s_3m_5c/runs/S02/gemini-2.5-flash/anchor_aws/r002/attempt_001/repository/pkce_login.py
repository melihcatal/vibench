import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode
import requests

from identity_models import PkceLoginConfig, TokenExchangeResponse
from identity_client import load_pkce_login_config

def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(64)
    # Auth0 PKCE code challenge method is S256
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest()).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

def start_pkce_login(payload, config=None):
    config: PkceLoginConfig = config or load_pkce_login_config()
    
    code_verifier, code_challenge = generate_pkce_challenge()
    state = secrets.token_urlsafe(32)

    # Auth0 specific authorization endpoint
    authorization_url_base = f"https://{config.domain}/authorize"

    query = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": payload.get("redirect_uri", config.redirect_uri),
        "scope": config.scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256", # Auth0 uses S256
    }
    if config.audience:
        query["audience"] = config.audience

    return {
        "authorization_url": authorization_url_base + "?" + urlencode(query),
        "session_id": state,
        "code_verifier": code_verifier # Store this in session for later use
    }

def exchange_pkce_code_for_tokens(code: str, code_verifier: str, redirect_uri: str) -> TokenExchangeResponse:
    config: PkceLoginConfig = load_pkce_login_config()

    # Auth0 specific token endpoint
    token_url = f"https://{config.domain}/oauth/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=urlencode(data))
    response.raise_for_status()
    token_data = response.json()

    return TokenExchangeResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
    )
