import os
import secrets
import hashlib
import base64
import urllib.parse
from typing import Dict, Optional
from identity_client import IdentityClient
from identity_models import PKCELoginRequest, PKCELoginResponse


def start_pkce_login(request: PKCELoginRequest) -> PKCELoginResponse:
    client = IdentityClient()

    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .replace("=", "")
    )

    state = secrets.token_urlsafe(32)
    nonce = secrets.token_urlsafe(32) if request.use_oidc else None

    params = {
        "client_id": client.client_id,
        "response_type": "code",
        "scope": " ".join(request.scopes),
        "redirect_uri": request.redirect_uri,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    if nonce:
        params["nonce"] = nonce

    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
    )

    client.store_state(
        state,
        {
            "code_verifier": code_verifier,
            "nonce": nonce,
            "redirect_uri": request.redirect_uri,
            "scopes": request.scopes,
            "client_id": client.client_id,
            "provider": "google",
        },
    )

    return PKCELoginResponse(
        authorization_url=auth_url,
        state=state,
        code_verifier=code_verifier,
        code_challenge=code_challenge,
        nonce=nonce,
        provider="google",
    )
