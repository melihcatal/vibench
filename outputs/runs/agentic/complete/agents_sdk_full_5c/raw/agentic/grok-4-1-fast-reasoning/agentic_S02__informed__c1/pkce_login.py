import os
import webbrowser
from typing import Tuple
from identity_client import generate_pkce_verifier_and_challenge, build_authorize_url
from identity_models import TokenResponse

def start_pkce_login(redirect_uri: str, scope: str = 'openid profile email', state: str = None) -> Tuple[str, str]:
    domain = os.getenv('AUTH0_DOMAIN')
    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable not set")
    client_id = os.getenv('AUTH0_CLIENT_ID')
    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable not set")
    authorize_endpoint = f"https://{domain}/authorize"
    verifier, challenge = generate_pkce_verifier_and_challenge()
    auth_url = build_authorize_url(authorize_endpoint, client_id, redirect_uri, scope, state, challenge)
    webbrowser.open(auth_url)
    print(f"PKCE login started. Store verifier for callback: {verifier[:20]}...")
    return auth_url, verifier

# Exchange with handle_oauth_callback(..., code_verifier=verifier)
