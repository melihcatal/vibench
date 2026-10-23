import os
import secrets
import hashlib
import base64
from authlib.integrations.httpx_client import OAuth2Client
from identity_client import get_auth0_config

def generate_pkce_challenge():
    """Generates a code verifier and its corresponding S256 code challenge."""
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def start_auth0_pkce_flow():
    """
    Starts an OAuth 2.0 Authorization Code flow with PKCE for a public client
    using Auth0.
    """
    config = get_auth0_config()
    client = OAuth2Client(
        client_id=config['client_id'],
        scope="openid profile email",
        redirect_uri=config['redirect_uri'],
        metadata_url=config['metadata_url']
    )

    code_verifier, code_challenge = generate_pkce_challenge()

    # PKCE-specific parameters
    auth_url_params = {
        "audience": config.get("audience"),
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    
    authorization_url, state = client.create_authorization_url(
        redirect_uri=config['redirect_uri'],
        **auth_url_params
    )
    
    # In a real app, the code_verifier and state would be stored in the user's session
    # to be retrieved during the callback.
    return {
        "authorization_url": authorization_url,
        "code_verifier": code_verifier, # Must be sent in token exchange
        "state": state
    }

def exchange_auth0_pkce_code(code: str, code_verifier: str):
    """
    Exchanges an authorization code for tokens using PKCE.
    This would be called in the callback handler.
    """
    config = get_auth0_config()
    client = OAuth2Client(
        client_id=config['client_id'],
        metadata_url=config['metadata_url']
    )

    token = client.fetch_token(
        grant_type='authorization_code',
        code=code,
        redirect_uri=config['redirect_uri'],
        code_verifier=code_verifier # PKCE requirement
    )
    return token
