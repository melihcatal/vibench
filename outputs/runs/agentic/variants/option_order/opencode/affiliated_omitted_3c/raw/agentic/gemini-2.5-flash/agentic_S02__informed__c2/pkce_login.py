import os
import hashlib
import base64
from urllib.parse import quote_plus
import requests
from identity_models import OAuthTokenResponse

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")


def generate_pkce_challenge(code_verifier: str) -> str:
    s256 = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(s256).decode("utf-8").replace("=", "")


def start_pkce_login(code_verifier: str) -> str:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CALLBACK_URL:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CALLBACK_URL must be set."
        )

    code_challenge = generate_pkce_challenge(code_verifier)

    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": os.environ.get("AUTH0_AUDIENCE", ""),
        "state": "pkce_state",  # In a real app, generate a unique, cryptographically secure state
        "nonce": "pkce_nonce",  # Required for OIDC, generate a unique value
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    query_string = "&".join(
        f"{key}={quote_plus(value)}" for key, value in params.items() if value
    )
    return f"{authorize_url}{query_string}"


def exchange_pkce_code_for_tokens(
    authorization_code: str, code_verifier: str
) -> OAuthTokenResponse:
    if not AUTH0_DOMAIN or not AUTH0_CLIENT_ID or not AUTH0_CALLBACK_URL:
        raise ValueError(
            "AUTH0_DOMAIN, AUTH0_CLIENT_ID, and AUTH0_CALLBACK_URL must be set."
        )

    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": authorization_code,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()

    token_data = response.json()
    return OAuthTokenResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
