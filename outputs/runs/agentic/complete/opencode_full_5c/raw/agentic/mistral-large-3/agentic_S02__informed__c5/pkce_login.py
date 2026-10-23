# Federated Login Flow - PKCE Login Flow

import os
import urllib.parse
from typing import Dict, Tuple
from identity_client import IdentityClient


def pkce_login(
    redirect_uri: str, state: str, scope: str = "openid profile email"
) -> Tuple[str, str]:
    """Implement Auth0 PKCE login flow for public clients."""
    client = IdentityClient()
    code_verifier, code_challenge = client.generate_pkce_pair()

    params = {
        "response_type": "code",
        "client_id": client.client_id,
        "redirect_uri": redirect_uri,
        "state": state,
        "scope": scope,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "audience": client.audience,
    }
    auth_url = f"{client.authorization_endpoint}?{urllib.parse.urlencode(params)}"
    return auth_url, code_verifier
