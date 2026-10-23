import os
import requests

from identity_client import get_auth0_domain, get_auth0_client_id
from identity_models import (
    build_password_reset_payload,
    normalize_password_reset_response,
)


def password_reset(email):
    domain = get_auth0_domain()
    url = f"https://{domain}/dbconnections/change_password"

    payload = build_password_reset_payload(
        email=email,
        client_id=get_auth0_client_id(),
        connection="Username-Password-Authentication",
    )

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    return normalize_password_reset_response(response.text if response.text else {})
