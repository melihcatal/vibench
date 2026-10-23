from __future__ import annotations

import requests

from identity_client import AUTH0_CLIENT_ID, AUTH0_DOMAIN, auth0_base_url, auth0_headers
from identity_models import RegisterUserRequest, LifecycleResponse


def register_user(
    email: str, password: str, display_name: str | None = None
) -> LifecycleResponse:
    req = RegisterUserRequest(
        email=email, password=password, display_name=display_name
    ).normalized()
    resp = requests.post(
        f"{auth0_base_url()}/api/v2/users",
        headers=auth0_headers(),
        json={
            "email": req.email,
            "password": req.password,
            "connection": "Username-Password-Authentication",
            "name": req.display_name or req.email.split("@")[0],
            "client_id": AUTH0_CLIENT_ID,
        },
        timeout=30,
    )
    if resp.ok:
        return LifecycleResponse(
            ok=True, provider=f"auth0:{AUTH0_DOMAIN}", data=resp.json()
        )
    return LifecycleResponse(
        ok=False, provider=f"auth0:{AUTH0_DOMAIN}", error=resp.text
    )
