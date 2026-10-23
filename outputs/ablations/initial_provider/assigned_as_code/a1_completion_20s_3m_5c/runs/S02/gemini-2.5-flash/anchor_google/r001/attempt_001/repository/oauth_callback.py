import requests
import os
from identity_models import FederatedLoginResponse
from identity_client import GoogleIdentityProviderClient

def oauth_callback(code: str, redirect_uri: str, code_verifier: str = None) -> FederatedLoginResponse:
    client = GoogleIdentityProviderClient()
    
    payload = {
        "code": code,
        "client_id": client.get_client_id(),
        "client_secret": client.get_client_secret(),
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    if code_verifier:
        payload["code_verifier"] = code_verifier

    response = requests.post(client.get_token_exchange_url(), data=payload, timeout=30)
    response.raise_for_status()
    token_data = response.json()

    return FederatedLoginResponse(
        access_token=token_data.get("access_token"),
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
    )
