from __future__ import annotations

import os
from urllib.parse import urlencode

from identity_client import AUTH0_CLIENT_ID, AUTH0_DOMAIN, AUTH0_REDIRECT_URI
from identity_models import LoginRequest


def start_oauth_login() -> str:
    request = LoginRequest(
        issuer=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=AUTH0_REDIRECT_URI,
        scopes=("openid", "profile", "email"),
    )
    params = {
        "response_type": "code",
        "client_id": request.client_id,
        "redirect_uri": request.redirect_uri,
        "scope": " ".join(request.scopes),
        "state": os.getenv("AUTH0_STATE", "login-state"),
        "nonce": os.getenv("AUTH0_NONCE", "login-nonce"),
    }
    return f"https://{request.issuer}/authorize?{urlencode(params)}"
