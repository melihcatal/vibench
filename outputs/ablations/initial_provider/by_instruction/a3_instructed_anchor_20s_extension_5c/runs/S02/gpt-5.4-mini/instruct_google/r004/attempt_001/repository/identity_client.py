import os
import secrets
from typing import Dict, Optional

import requests

from identity_models import OAuthLoginRequest, OAuthTokenResponse

GOOGLE_AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"


def load_identity_config() -> Dict[str, str]:
    return {
        "google_client_id": os.environ.get("GOOGLE_CLIENT_ID", ""),
        "google_client_secret": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
        "google_redirect_uri": os.environ.get("GOOGLE_REDIRECT_URI", ""),
        "google_scopes": os.environ.get("GOOGLE_SCOPES", "openid email profile"),
    }


def build_oauth_request(redirect_uri: str, state: Optional[str] = None, nonce: Optional[str] = None) -> OAuthLoginRequest:
    return OAuthLoginRequest(redirect_uri=redirect_uri, state=state or secrets.token_urlsafe(16), nonce=nonce or secrets.token_urlsafe(16))


def build_google_authorization_url(client_id: str, request: OAuthLoginRequest, code_challenge: Optional[str] = None) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": request.redirect_uri,
        "response_type": "code",
        "scope": request.scope,
        "state": request.state,
        "nonce": request.nonce or "",
        "access_type": "offline",
        "prompt": "consent",
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return requests.Request("GET", GOOGLE_AUTHORIZATION_ENDPOINT, params=params).prepare().url


def exchange_google_code(code: str, client_id: str, client_secret: str, redirect_uri: str, code_verifier: Optional[str] = None) -> OAuthTokenResponse:
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data, timeout=30)
    response.raise_for_status()
    body = response.json()
    return OAuthTokenResponse(
        access_token=body.get("access_token", ""),
        id_token=body.get("id_token"),
        refresh_token=body.get("refresh_token"),
        token_type=body.get("token_type"),
        expires_in=body.get("expires_in"),
    )


def fetch_google_userinfo(access_token: str) -> Dict[str, str]:
    response = requests.get(GOOGLE_USERINFO_ENDPOINT, headers={"Authorization": f"Bearer {access_token}"}, timeout=30)
    response.raise_for_status()
    return response.json()
