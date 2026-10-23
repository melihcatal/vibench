import os
import secrets
import urllib.parse
from typing import Dict, Optional
from identity_client import IdentityClient
from identity_models import OAuthStartRequest, OAuthStartResponse


def start_oauth_login(request: OAuthStartRequest) -> OAuthStartResponse:
    client = IdentityClient()

    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32) if request.use_oidc else None

    auth_url = client.build_authorization_url(
        state=state,
        nonce=nonce,
        scopes=request.scopes,
        redirect_uri=request.redirect_uri,
    )

    client.store_state(
        state,
        {
            "nonce": nonce,
            "redirect_uri": request.redirect_uri,
            "scopes": request.scopes,
            "client_id": client.client_id,
            "provider": "google",
        },
    )

    return OAuthStartResponse(
        authorization_url=auth_url, state=state, nonce=nonce, provider="google"
    )
