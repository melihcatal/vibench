import os
import base64
import hashlib
import secrets
from urllib.parse import urlencode
import requests
from identity_client import get_auth0_config
from identity_models import AuthTokens

def generate_pkce_challenge() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(96)
    s256 = hashlib.sha256()
    s256.update(code_verifier.encode("utf-8"))
    code_challenge = base64.urlsafe_b64encode(s256.digest()).decode("utf-8").replace("=", "")
    return code_verifier, code_challenge

def pkce_login_start(redirect_uri: str, state: str) -> dict:
    auth0_config = get_auth0_config()
    domain = auth0_config["DOMAIN"]
    client_id = auth0_config["CLIENT_ID"]

    code_verifier, code_challenge = generate_pkce_challenge()

    authorize_url = f"https://{domain}/authorize"
    params = {
        "response_type": "code",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
    }
    url = f"{authorize_url}?{urlencode(params)}"
    
    return {
        "authorization_url": url,
        "code_verifier": code_verifier, # Store this in session for later use
        "session_id": state,
    }

def pkce_login_callback(code: str, code_verifier: str, redirect_uri: str, state: str, session_state: str) -> AuthTokens:
    auth0_config = get_auth0_config()
    domain = auth0_config["DOMAIN"]
    client_id = auth0_config["CLIENT_ID"]

    if state != session_state:
        raise ValueError("State mismatch. Possible CSRF attack.")

    token_url = f"https://{domain}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=urlencode(payload))
    response.raise_for_status()
    token_data = response.json()

    return AuthTokens(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
    )
