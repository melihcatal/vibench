from __future__ import annotations

import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

from identity_client import get_provider_config, build_authorization_url
from identity_models import AuthRequest, build_pkce_pair


MICROSOFT_AUTHORIZE_HOST = "login.microsoftonline.com"


def start_pkce_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile offline_access",
) -> Dict[str, str]:
    config = get_provider_config()
    authorization_endpoint = config.authorization_endpoint or f"https://{MICROSOFT_AUTHORIZE_HOST}/common/oauth2/v2.0/authorize"
    client_id = client_id or config.client_id or os.environ.get("AZURE_CLIENT_ID", "demo-client-id")
    redirect_uri = redirect_uri or config.redirect_uri or "com.example.app:/oauth/callback"
    state = secrets.token_urlsafe(24)
    verifier, challenge = build_pkce_pair()
    nonce = secrets.token_urlsafe(24)
    request = AuthRequest(
        provider="microsoft",
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        state=state,
        nonce=nonce,
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    return {
        "authorization_url": build_authorization_url(authorization_endpoint, request),
        "state": state,
        "nonce": nonce,
        "code_verifier": verifier,
    }


if __name__ == "__main__":
    print(start_pkce_login())
