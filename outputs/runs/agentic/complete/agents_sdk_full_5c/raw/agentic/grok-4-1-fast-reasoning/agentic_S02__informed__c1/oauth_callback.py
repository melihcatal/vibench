import os
from typing import Optional
from identity_client import exchange_authorization_code
from identity_models import TokenResponse

def handle_oauth_callback(code: str, redirect_uri: str, client_secret: Optional[str] = None, code_verifier: Optional[str] = None) -> TokenResponse:
    domain = os.getenv('AUTH0_DOMAIN')
    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable not set")
    client_id = os.getenv('AUTH0_CLIENT_ID')
    token_endpoint = f"https://{domain}/oauth/token"
    client_secret = os.getenv('AUTH0_CLIENT_SECRET') if client_secret is None else client_secret
    tokens = exchange_authorization_code(token_endpoint, client_id, code, redirect_uri, client_secret, code_verifier)
    return tokens
