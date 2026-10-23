import os
import requests

from identity_client import (
    get_auth0_domain,
    get_auth0_client_id,
    get_auth0_client_secret,
)
from identity_models import build_login_payload, normalize_login_response


def email_password_login(email, password):
    domain = get_auth0_domain()
    url = f"https://{domain}/oauth/token"

    payload = build_login_payload(
        email=email,
        password=password,
        client_id=get_auth0_client_id(),
        client_secret=get_auth0_client_secret(),
        audience=f"https://{domain}/api/v2/",
    )

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()

    return normalize_login_response(response.json())
