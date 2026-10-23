# Federated Login Flow - OAuth Callback Handler

import os
from typing import Dict
from identity_client import IdentityClient


def oauth_callback(code: str, redirect_uri: str, code_verifier: str) -> Dict:
    """Handle Auth0 OIDC callback and exchange code for tokens."""
    client = IdentityClient()
    token_response = client.get_oauth_token(code, redirect_uri, code_verifier)
    return token_response
