import requests

from identity_client import Auth0Client
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    client = Auth0Client()
    payload = RefreshRequest(refresh_token=refresh_token)
    response = requests.post(
        f"{client.base_url}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "client_id": client.client_id,
            "refresh_token": payload.refresh_token,
        },
        headers=client.headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
