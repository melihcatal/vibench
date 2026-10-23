import os
import secrets
import requests
from urllib.parse import urlencode
from identity_client import generate_pkce_pair
from identity_models import TokenResponse

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8080/callback")


def pkce_start_login(state: str = None) -> tuple[str, str, str]:
    if state is None:
        state = secrets.token_urlsafe(32)
    verifier, challenge = generate_pkce_pair()
    params = {
        "client_id": GITHUB_CLIENT_ID,
        "redirect_uri": GITHUB_REDIRECT_URI,
        "scope": "user:email",
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"
    return auth_url, state, verifier


def pkce_exchange(code: str, verifier: str) -> TokenResponse:
    data = {
        "client_id": GITHUB_CLIENT_ID,
        "code": code,
        "code_verifier": verifier,
        "redirect_uri": GITHUB_REDIRECT_URI,
    }
    response = requests.post(
        GITHUB_TOKEN_URL, data=data, headers={"Accept": "application/json"}
    )
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(
        access_token=tokens["access_token"],
        token_type="bearer",
        expires_in=3600 * 24 * 365 * 10,
        scope=tokens.get("scope", ""),
    )
