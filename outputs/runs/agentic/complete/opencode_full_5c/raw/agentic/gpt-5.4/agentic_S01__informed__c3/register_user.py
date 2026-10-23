import requests

from identity_client import (
    auth0_connection,
    auth0_domain,
    auth0_headers,
    auth0_management_token,
    request_timeout,
)
from identity_models import (
    RegisterUserRequest,
    auth0_user_payload,
    normalize_auth0_user,
)


def register_user(request: RegisterUserRequest):
    token = auth0_management_token()
    payload = auth0_user_payload(request, auth0_connection())
    response = requests.post(
        f"https://{auth0_domain()}/api/v2/users",
        headers=auth0_headers(token),
        json=payload,
        timeout=request_timeout(),
    )
    response.raise_for_status()
    return normalize_auth0_user(response.json())
