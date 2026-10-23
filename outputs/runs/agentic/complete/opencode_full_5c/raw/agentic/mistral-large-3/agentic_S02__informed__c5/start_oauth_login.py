# Federated Login Flow - Start OAuth Login

import os
import urllib.parse
from typing import Dict
from identity_client import IdentityClient


def start_oauth_login(
    redirect_uri: str, state: str, scope: str = "openid profile email"
) -> str:
    """Start Auth0 OIDC authorization-code login."""
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
    return auth_url
