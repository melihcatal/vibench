import os
from typing import Any, Dict, Optional

import requests


GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> Dict[str, Any]:
    client_id = os.environ["GOOGLE_CLIENT_ID"]
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    if client_secret:
        payload["client_secret"] = client_secret
    response = requests.post(
        GOOGLE_TOKEN_ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
