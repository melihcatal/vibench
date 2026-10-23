from __future__ import annotations

import requests

from identity_client import AUTH0_DOMAIN, auth0_base_url, auth0_token_payload
from identity_models import LoginRequest, LifecycleResponse


def email_password_login(email: str, password: str) -> LifecycleResponse:
    req = LoginRequest(email=email, password=password).normalized()
    resp = requests.post(
        f"{auth0_base_url()}/oauth/token",
        headers={"Content-Type": "application/json"},
        json=auth0_token_payload(
            "password",
            username=req.email,
            password=req.password,
            scope="openid profile email offline_access",
        ),
        timeout=30,
    )
    if resp.ok:
        return LifecycleResponse(
            ok=True, provider=f"auth0:{AUTH0_DOMAIN}", data=resp.json()
        )
    return LifecycleResponse(
        ok=False, provider=f"auth0:{AUTH0_DOMAIN}", error=resp.text
    )
