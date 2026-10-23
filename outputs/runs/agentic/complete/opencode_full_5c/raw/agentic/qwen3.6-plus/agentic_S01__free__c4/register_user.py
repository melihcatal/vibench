import os
import requests

from identity_client import (
    get_auth0_domain,
    get_auth0_client_id,
    get_auth0_management_token,
)
from identity_models import build_register_payload, normalize_register_response


def register_user(email, password, user_metadata=None):
    domain = get_auth0_domain()
    url = f"https://{domain}/api/v2/users"

    token = get_auth0_management_token()

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    payload = build_register_payload(
        email=email,
        password=password,
        connection="Username-Password-Authentication",
        user_metadata=user_metadata or {},
    )

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    return normalize_register_response(response.json())
