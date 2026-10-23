import os
from typing import Any

import requests

from identity_client import get_identity_config, normalize_id_token_claims
from identity_models import CallbackExchangeRequest, TokenSet


def oauth_callback(request: CallbackExchangeRequest) -> TokenSet:
    config = get_identity_config()
    token_url = config.token_endpoint
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": request.code,
        "redirect_uri": request.redirect_uri,
    }
    if request.code_verifier:
        data["code_verifier"] = request.code_verifier
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=data, headers=headers, timeout=20)
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    claims = normalize_id_token_claims(payload.get("id_token"), issuer=config.issuer)
    return TokenSet(
        access_token=payload.get("access_token", ""),
        id_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        token_type=payload.get("token_type"),
        scope=payload.get("scope"),
        claims=claims,
    )
