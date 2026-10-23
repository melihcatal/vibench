from __future__ import annotations

import os
from typing import Dict

from identity_client import AUTH0_CLIENT_ID, build_authorize_url, create_pkce_pair
from identity_models import OIDCLoginRequest


def start_login(redirect_uri: str, state: str, nonce: str) -> Dict[str, str]:
    request = OIDCLoginRequest(
        provider="auth0",
        client_id=AUTH0_CLIENT_ID,
        redirect_uri=redirect_uri,
        state=state,
        nonce=nonce,
    )
    verifier, challenge = create_pkce_pair()
    request.code_challenge = challenge
    return {
        "authorization_url": build_authorize_url(request),
        "code_verifier": verifier,
    }
