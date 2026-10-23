from __future__ import annotations

import base64
import hashlib
import os
import secrets
from urllib.parse import urlencode

from identity_client import get_identity_settings
from identity_models import PKCELoginRequest

AZURE_AUTHORIZE_ENDPOINT = "https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize"


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def generate_pkce_pair() -> tuple[str, str]:
    verifier = _b64url(secrets.token_bytes(32))
    challenge = _b64url(hashlib.sha256(verifier.encode("ascii")).digest())
    return verifier, challenge


def build_pkce_login_url(request: PKCELoginRequest) -> tuple[str, str]:
    settings = get_identity_settings()
    verifier, challenge = generate_pkce_pair()
    params = {
        "client_id": settings.client_id,
        "response_type": "code",
        "redirect_uri": request.redirect_uri or settings.redirect_uri,
        "scope": request.scope or settings.scopes,
        "state": request.state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "response_mode": "query",
    }
    if request.prompt:
        params["prompt"] = request.prompt
    return f"{AZURE_AUTHORIZE_ENDPOINT.format(tenant_id=settings.azure_tenant_id)}?{urlencode(params)}", verifier


def pkce_login(request: PKCELoginRequest) -> dict[str, str]:
    url, verifier = build_pkce_login_url(request)
    return {"authorization_url": url, "code_verifier": verifier}


if __name__ == "__main__":
    state = os.getenv("PKCE_STATE", "example-state")
    login = pkce_login(PKCELoginRequest(state=state, redirect_uri=os.getenv("PKCE_REDIRECT_URI")))
    print(login["authorization_url"])
