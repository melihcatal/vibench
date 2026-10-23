from __future__ import annotations

import requests

from identity_client import (
    auth0_headers,
    get_auth0_management_token,
    get_auth0_settings,
)
from identity_models import RegisterUserRequest, UserAccount


def register_user(request: RegisterUserRequest) -> UserAccount:
    settings = get_auth0_settings()
    management_token = get_auth0_management_token()
    response = requests.post(
        f"https://{settings['domain']}/api/v2/users",
        headers=auth0_headers(management_token),
        json=request.to_auth0_payload(settings["connection"]),
        timeout=30,
    )
    response.raise_for_status()
    return UserAccount.from_auth0(response.json())
