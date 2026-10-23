import os
import base64
import hashlib
from urllib.parse import urlencode
import requests
from identity_client import get_auth0_config
from identity_models import TokenResponse


def generate_pkce_challenge() -> tuple[str, str]:
    code_verifier = (
        base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")
    )
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return code_verifier, code_challenge


def start_pkce_login() -> tuple[str, str]:
    config = get_auth0_config()
    if not config.domain or not config.client_id or not config.redirect_uri:
        raise ValueError("Auth0 domain, client ID, or redirect URI not configured.")

    code_verifier, code_challenge = generate_pkce_challenge()

    authorize_url = f"https://{config.domain}/authorize"
    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "redirect_uri": config.redirect_uri,
        "scope": "openid profile email",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{authorize_url}?{urlencode(params)}", code_verifier


def handle_pkce_callback(code: str, code_verifier: str) -> TokenResponse:
    config = get_auth0_config()
    if not config.domain or not config.client_id or not config.redirect_uri:
        raise ValueError("Auth0 domain, client ID, or redirect URI not configured.")

    token_url = f"https://{config.domain}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": code,
        "redirect_uri": config.redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()

    return TokenResponse(
        access_token=token_data.get("access_token", ""),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
