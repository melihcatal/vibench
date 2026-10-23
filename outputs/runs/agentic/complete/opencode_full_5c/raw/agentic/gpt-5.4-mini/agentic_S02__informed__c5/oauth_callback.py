import requests

from identity_client import load_identity_config, token_endpoint
from identity_models import TokenResponse


def exchange_code_for_tokens(
    code: str, redirect_uri: str, code_verifier: str | None = None
) -> TokenResponse:
    config = load_identity_config("AUTH0")
    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        payload["code_verifier"] = code_verifier
    response = requests.post(token_endpoint(config), json=payload, timeout=20)
    response.raise_for_status()
    data = response.json()
    return TokenResponse(
        access_token=data["access_token"],
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type"),
        expires_in=data.get("expires_in"),
    )
