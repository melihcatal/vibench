import os
from typing import Any, Dict

import requests


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(code: str, redirect_uri: str) -> Dict[str, Any]:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
    payload = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def handle_callback(query_params: Dict[str, str], redirect_uri: str) -> Dict[str, Any]:
    if "error" in query_params:
        raise ValueError(query_params["error"])
    code = query_params.get("code")
    if not code:
        raise ValueError("Missing authorization code")
    return exchange_authorization_code(code, redirect_uri)
