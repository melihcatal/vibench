import os
import requests
from identity_client import Auth0Client
from identity_models import RefreshTokenRequest, RefreshTokenResponse


def refresh_session(refresh_token: str) -> RefreshTokenResponse:
    client = Auth0Client()
    url = f"https://{client.domain}/oauth/token"
    payload = RefreshTokenRequest(
        refresh_token=refresh_token, client_id=client.client_id
    ).dict()
    payload["grant_type"] = "refresh_token"

    response = requests.post(url, json=payload, headers=client.headers)
    response.raise_for_status()
    data = response.json()

    return RefreshTokenResponse(**data)
