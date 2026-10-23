import os
from typing import Dict, Optional

import requests

from identity_models import OAuthLoginRequest, OAuthTokenResponse


AZURE_AD_AUTHORITY = os.getenv("AZURE_AD_AUTHORITY", "https://login.microsoftonline.com/common")
AZURE_AD_CLIENT_ID = os.getenv("AZURE_AD_CLIENT_ID", "")
AZURE_AD_CLIENT_SECRET = os.getenv("AZURE_AD_CLIENT_SECRET", "")
AZURE_AD_SCOPE = os.getenv("AZURE_AD_SCOPE", "openid profile email offline_access")


def build_authorization_url(request: OAuthLoginRequest, code_challenge: Optional[str] = None) -> str:
    params = {
        "client_id": AZURE_AD_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": request.redirect_uri,
        "scope": request.scope or AZURE_AD_SCOPE,
    }
    if request.state:
        params["state"] = request.state
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    query = "&".join(f"{k}={requests.utils.quote(str(v))}" for k, v in params.items())
    return f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/authorize?{query}"


def exchange_code_for_token(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> OAuthTokenResponse:
    data: Dict[str, str] = {
        "client_id": AZURE_AD_CLIENT_ID,
        "client_secret": AZURE_AD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/token", data=data, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return OAuthTokenResponse(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        token_type=payload.get("token_type"),
        raw=payload,
    )
