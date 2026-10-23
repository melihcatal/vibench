import requests

from identity_client import AUTH0_CLIENT_ID, base_url, passwordless_headers
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    payload = RefreshRequest(refresh_token=refresh_token).to_dict()
    response = requests.post(
        f"{base_url()}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "client_id": AUTH0_CLIENT_ID,
            "refresh_token": payload["refresh_token"],
        },
        headers=passwordless_headers(),
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
