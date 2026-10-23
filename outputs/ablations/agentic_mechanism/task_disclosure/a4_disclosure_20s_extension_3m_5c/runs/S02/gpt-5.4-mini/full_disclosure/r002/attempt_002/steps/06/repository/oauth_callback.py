import os
from typing import Any, Dict, Optional

import requests


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"


def exchange_authorization_code(
    code: str,
    redirect_uri: str,
    code_verifier: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> Dict[str, Any]:
    token_url = os.getenv("GOOGLE_OAUTH_TOKEN_URL", GOOGLE_TOKEN_URL)
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": client_id or os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    secret = client_secret or os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    if secret:
        payload["client_secret"] = secret
    response = requests.post(token_url, data=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def handle_callback(query_params: Dict[str, str], redirect_uri: str) -> Dict[str, Any]:
    if "error" in query_params:
        raise ValueError(query_params["error"])
    code = query_params.get("code")
    if not code:
        raise ValueError("Missing authorization code")
    return exchange_authorization_code(
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=query_params.get("code_verifier"),
    )
