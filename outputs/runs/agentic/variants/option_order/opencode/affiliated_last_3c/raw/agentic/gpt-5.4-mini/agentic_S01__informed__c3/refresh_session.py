import os

import requests

from identity_client import auth0_domain
from identity_models import TokenSet


def refresh_session(refresh_token: str) -> TokenSet:
    resp = requests.post(
        f"https://{auth0_domain()}/oauth/token",
        json={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": os.environ.get("AUTH0_CLIENT_ID", ""),
            "client_secret": os.environ.get("AUTH0_CLIENT_SECRET", ""),
        },
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    return TokenSet(
        access_token=data["access_token"],
        refresh_token=data.get("refresh_token", refresh_token),
        id_token=data.get("id_token"),
        expires_in=data.get("expires_in"),
    )
