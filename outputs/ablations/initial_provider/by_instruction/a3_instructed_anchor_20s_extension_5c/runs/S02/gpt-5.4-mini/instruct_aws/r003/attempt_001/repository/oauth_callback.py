import base64
import hashlib
import os
import urllib.parse
import requests

from identity_client import load_identity_config
from identity_models import OAuthTokenResponse


def exchange_code_for_tokens(code: str) -> OAuthTokenResponse:
    cfg = load_identity_config()
    token_url = f"https://{cfg['cognito_domain']}/oauth2/token"
    auth = base64.b64encode(f"{cfg['cognito_user_pool_client_id']}:{cfg['cognito_user_pool_client_secret']}".encode()).decode()
    response = requests.post(
        token_url,
        data={"grant_type": "authorization_code", "code": code, "redirect_uri": cfg["redirect_uri"]},
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    payload = response.json()
    return OAuthTokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=payload.get("expires_in"),
        raw=payload,
    )
