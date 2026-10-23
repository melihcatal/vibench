from __future__ import annotations

import requests

from identity_client import AUTH0_DOMAIN, auth0_base_url
from identity_models import PasswordResetRequest, LifecycleResponse


def password_reset(email: str) -> LifecycleResponse:
    req = PasswordResetRequest(email=email).normalized()
    resp = requests.post(
        f"{auth0_base_url()}/dbconnections/change_password",
        headers={"Content-Type": "application/json"},
        json={
            "client_id": "",
            "email": req.email,
            "connection": "Username-Password-Authentication",
        },
        timeout=30,
    )
    if resp.ok:
        return LifecycleResponse(
            ok=True, provider=f"auth0:{AUTH0_DOMAIN}", data={"message": resp.text}
        )
    return LifecycleResponse(
        ok=False, provider=f"auth0:{AUTH0_DOMAIN}", error=resp.text
    )
