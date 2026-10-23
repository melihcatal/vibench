import secrets
from urllib.parse import urlencode
import hashlib
import base64

from identity_client import IdentityClient, get_identity_client_config
from identity_models import PkceLoginRequest

def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(96)  # Generate a high-entropy cryptographically random string
    # S256 code_challenge_method
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def start_pkce_login(payload: PkceLoginRequest):
    config = get_identity_client_config()
    client = IdentityClient(config['tenant_id'], config['client_id'], config['client_secret'])
    msal_app = client.get_msal_app()

    state = payload.state or secrets.token_urlsafe(32)

    # MSAL doesn't directly expose a PKCE-specific `get_authorization_request_url`
    # that takes code_challenge and code_challenge_method as direct args for public clients.
    # For public clients (which PKCE is designed for), MSAL handles PKCE internally.
    # However, since start_oauth_login.py is using ConfidentialClientApplication,
    # and we are mimicking a similar flow, we'll construct the URL manually with PKCE parameters.
    # In a real public client, msal.PublicClientApplication would be used and would simplify this.

    # Construct the authorization URL with PKCE parameters
    # Azure AD supports PKCE for confidential clients if configured correctly, but it's primarily for public clients.
    # For this exercise, we'll add the PKCE params to the URL.
    query_params = {
        'client_id': config['client_id'],
        'response_type': 'code',
        'redirect_uri': payload.redirect_uri,
        'scope': ' '.join(payload.scopes),
        'state': state,
        'code_challenge': payload.code_challenge,
        'code_challenge_method': payload.code_challenge_method,
    }
    
    authorization_url = f"{client.authority}/oauth2/v2.0/authorize?{urlencode(query_params)}"
    
    return {'authorization_url': authorization_url, 'session_id': state, 'code_verifier': payload.code_challenge} # Returning code_challenge for demonstration
