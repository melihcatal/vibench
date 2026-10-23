import base64
import json
from urllib.parse import parse_qs

import requests

from identity_client import token_endpoint, client_id, client_secret, redirect_uri
from identity_models import OAuthTokenResponse


def exchange_code(code: str, code_verifier: str = None) -> OAuthTokenResponse:
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": redirect_uri() or "", "client_id": client_id() or ""}
    if code_verifier:
        data["code_verifier"] = code_verifier
    auth = None
    if client_secret():
        auth = (client_id() or "", client_secret() or "")
    response = requests.post(token_endpoint() or "", data=data, auth=auth, timeout=30)
    response.raise_for_status()
    payload = response.json()
    return OAuthTokenResponse(access_token=payload["access_token"], id_token=payload.get("id_token"), refresh_token=payload.get("refresh_token"), token_type=payload.get("token_type"), expires_in=payload.get("expires_in"))
