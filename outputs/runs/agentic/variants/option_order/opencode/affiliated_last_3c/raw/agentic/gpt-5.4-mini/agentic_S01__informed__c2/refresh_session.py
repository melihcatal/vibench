import requests

from identity_client import (
    auth0_headers,
    get_auth0_client_id,
    get_auth0_client_secret,
    get_auth0_domain,
)
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    req = RefreshRequest(refresh_token=refresh_token)
    response = requests.post(
        f"https://{get_auth0_domain()}/oauth/token",
        headers=auth0_headers(),
        json={
            "grant_type": "refresh_token",
            "refresh_token": req.as_dict()["refresh_token"],
            "client_id": get_auth0_client_id(),
            "client_secret": get_auth0_client_secret(),
        },
        timeout=30,
    )
    return response.json()
