import base64
import hashlib
import os
from urllib.parse import urlencode
from identity_client import get_auth0_client

def create_pkce_session_data() -> dict:
    """
    Generates a code verifier and code challenge for a PKCE flow.
    """
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    code_verifier = code_verifier.rstrip('=')

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.rstrip('=')
    
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge
    }

def get_pkce_authorize_url(session_state: str, code_challenge: str) -> str:
    """
    Generates an authorization URL for a PKCE flow.
    """
    auth0 = get_auth0_client()
    audience = 'https://your-api-identifier.com'
    
    params = {
        'redirect_uri': auth0.redirect_uri,
        'client_id': auth0.client_id,
        'response_type': 'code',
        'scope': 'openid profile email offline_access',
        'state': session_state,
        'audience': audience,
        'code_challenge_method': 'S256',
        'code_challenge': code_challenge,
    }
    
    return f"https://{auth0.domain}/authorize?{urlencode(params)}"

def exchange_pkce_code_for_tokens(authorization_code: str, code_verifier: str) -> dict:
    """
    Exchanges an authorization code for tokens using the PKCE code verifier.
    """
    auth0_get_token = get_auth0_client().get_token

    # Note: No client_secret is sent for a public client (e.g., SPA, mobile app)
    # using PKCE.
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': auth0_get_token.client_id,
        'code': authorization_code,
        'redirect_uri': auth0_get_token.redirect_uri,
        'code_verifier': code_verifier
    }
    
    token_info = auth0_get_token.authorization_code(token_payload)
    return token_info
