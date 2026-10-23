from __future__ import annotations

import requests

from identity_client import AUTH0_DOMAIN, auth0_base_url, auth0_token_payload
from identity_models import RefreshRequest, LifecycleResponse


def refresh_session(refresh_token: str) -> LifecycleResponse:
    req = RefreshRequest(refresh_token=refresh_token)
    resp = requests.post(
        f"{auth0_base_url()}/oauth/token",
        headers={"Content-Type": "application/json"},
        json=auth0_token_payload("refresh_token", refresh_token=req.refresh_token),
        timeout=30,
    )
    if resp.ok:
        return LifecycleResponse(
            ok=True, provider=f"auth0:{AUTH0_DOMAIN}", data=resp.json()
        )
    return LifecycleResponse(
        ok=False, provider=f"auth0:{AUTH0_DOMAIN}", error=resp.text
    )
