import os
import secrets
from urllib.parse import urlencode

import requests


def get_issuer_base_url() -> str:
    return os.getenv("OKTA_ISSUER", "https://dev-123456.okta.com/oauth2/default")


def get_client_id() -> str:
    return os.getenv("OKTA_CLIENT_ID", "okta-client-id")


def get_client_secret() -> str:
    return os.getenv("OKTA_CLIENT_SECRET", "okta-client-secret")


def get_redirect_uri() -> str:
    return os.getenv("OKTA_REDIRECT_URI", "https://app.example.com/oauth/callback")


def build_authorize_url(
    scope: str = "openid profile email", state: str = None, code_challenge: str = None
) -> str:
    params = {
        "client_id": get_client_id(),
        "response_type": "code",
        "scope": scope,
        "redirect_uri": get_redirect_uri(),
        "state": state or secrets.token_urlsafe(16),
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return f"{get_issuer_base_url()}/v1/authorize?{urlencode(params)}"


def token_endpoint() -> str:
    return f"{get_issuer_base_url()}/v1/token"


def jwks_endpoint() -> str:
    return f"{get_issuer_base_url()}/v1/keys"


def userinfo_endpoint() -> str:
    return f"{get_issuer_base_url()}/v1/userinfo"


def exchange_code_for_token(code: str, code_verifier: str = None) -> dict:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": get_redirect_uri(),
        "client_id": get_client_id(),
        "client_secret": get_client_secret(),
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(), data=data, timeout=20)
    response.raise_for_status()
    return response.json()


def fetch_userinfo(access_token: str) -> dict:
    response = requests.get(
        userinfo_endpoint(),
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=20,
    )
    response.raise_for_status()
    return response.json()
