import os
import requests
import hashlib
import base64
from urllib.parse import urlencode

from identity_client import OKTA_ORG_URL, OKTA_CLIENT_ID, OKTA_REDIRECT_URI

def generate_pkce_codes():
    """Generates a PKCE code_verifier and code_challenge."""
    verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')
    
    hashed = hashlib.sha256(verifier.encode('ascii')).digest()
    challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('ascii')
    
    return verifier, challenge

def start_okta_pkce_login(code_challenge: str, state: str, scope: str = "openid profile email") -> str:
    """Constructs the Okta authorization URL for the OAuth 2.0 PKCE flow."""
    auth_params = {
        "client_id": OKTA_CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": OKTA_REDIRECT_URI,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    
    # Okta's authorization endpoint
    authorization_url = f"{OKTA_ORG_URL}/oauth2/default/v1/authorize?{urlencode(auth_params)}"
    return authorization_url

def exchange_pkce_code_for_tokens(code: str, code_verifier: str) -> dict:
    """Exchanges an authorization code with PKCE for access and ID tokens with Okta."""
    token_endpoint = f"{OKTA_ORG_URL}/oauth2/default/v1/token"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = {
        "grant_type": "authorization_code",
        "client_id": OKTA_CLIENT_ID,
        "code": code,
        "redirect_uri": OKTA_REDIRECT_URI,
        "code_verifier": code_verifier,
    }

    response = requests.post(token_endpoint, headers=headers, data=data)
    response.raise_for_status()
    return response.json()
