from __future__ import annotations

import base64
import hashlib
import os
import secrets
import urllib.parse
from dataclasses import asdict
from typing import Dict, Optional

from identity_client import get_provider_config, build_authorization_url
from identity_models import AuthRequest, ensure_https_url


AUTH0_AUTH_HOST = "YOUR_TENANT.us.auth0.com"


def start_oauth_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
    state: Optional[str] = None,
    nonce: Optional[str] = None,
    code_challenge: Optional[str] = None,
) -> Dict[str, str]:
    config = get_provider_config()
    provider = config.provider_name or "auth0"
    authorization_endpoint = config.authorization_endpoint or f"https://{AUTH0_AUTH_HOST}/authorize"
    client_id = client_id or config.client_id or os.environ.get("AUTH0_CLIENT_ID", "demo-client-id")
    redirect_uri = ensure_https_url(redirect_uri or config.redirect_uri or "https://app.example.com/oauth/callback")
    state = state or secrets.token_urlsafe(24)
    nonce = nonce or secrets.token_urlsafe(24)

    if not code_challenge:
        verifier = secrets.token_urlsafe(48)
        digest = hashlib.sha256(verifier.encode("ascii")).digest()
        code_challenge = base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")
    else:
        verifier = os.environ.get("OAUTH_CODE_VERIFIER", "")

    request = AuthRequest(
        provider=provider,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        nonce=nonce,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    url = build_authorization_url(authorization_endpoint, request)
    return {"authorization_url": url, "state": state, "nonce": nonce, "code_verifier": verifier}


if __name__ == "__main__":
    result = start_oauth_login()
    print(result["authorization_url"])
