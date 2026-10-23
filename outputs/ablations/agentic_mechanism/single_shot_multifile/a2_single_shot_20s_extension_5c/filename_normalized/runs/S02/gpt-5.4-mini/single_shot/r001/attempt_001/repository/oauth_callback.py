import base64
import hashlib
from typing import Optional

import requests

from identity_client import get_identity_provider_config, load_pkce_state
from identity_models import OAuthCallbackRequest, OAuthTokenResponse

AUTH0_TOKEN_URL = "https://{domain}/oauth/token"


def _basic_auth_header(client_id: str, client_secret: str) -> str:
    token = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"


def exchange_authorization_code(request: OAuthCallbackRequest) -> OAuthTokenResponse:
    config = get_identity_provider_config()
    pkce = load_pkce_state(request.state)
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": request.code,
        "redirect_uri": request.redirect_uri or config.redirect_uri,
        "code_verifier": request.code_verifier or pkce.code_verifier,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": _basic_auth_header(config.client_id, config.client_secret),
    }
    response = requests.post(AUTH0_TOKEN_URL.format(domain=config.provider_domain), data=data, headers=headers, timeout=15)
    response.raise_for_status()
    payload = response.json()
    return OAuthTokenResponse(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token"),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=payload.get("expires_in"),
        scope=payload.get("scope"),
    )
