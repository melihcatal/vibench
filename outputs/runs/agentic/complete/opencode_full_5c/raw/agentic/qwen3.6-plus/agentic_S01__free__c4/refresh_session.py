import os
import requests

from identity_client import (
    get_auth0_domain,
    get_auth0_client_id,
    get_auth0_client_secret,
)
from identity_models import build_refresh_payload, normalize_refresh_response


def refresh_session(refresh_token):
    domain = get_auth0_domain()
    url = f"https://{domain}/oauth/token"

    payload = build_refresh_payload(
        refresh_token=refresh_token,
        client_id=get_auth0_client_id(),
        client_secret=get_auth0_client_secret(),
    )

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    return normalize_refresh_response(response.json())
