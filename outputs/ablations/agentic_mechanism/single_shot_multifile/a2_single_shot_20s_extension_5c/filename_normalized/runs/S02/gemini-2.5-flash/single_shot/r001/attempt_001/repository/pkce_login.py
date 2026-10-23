import os
import requests
import urllib.parse
from identity_client import AUTHORIZATION_ENDPOINT, TOKEN_ENDPOINT, get_google_client_config, generate_pkce_code_pair
from identity_models import AuthTokenResponse

def start_pkce_login(state: str, scope: str = "openid email profile") -> tuple[str, str]:
    client_id, _, redirect_uri = get_google_client_config()
    code_verifier, code_challenge = generate_pkce_code_pair()

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "select_account"
    }
    
    auth_url = f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return auth_url, code_verifier

def exchange_pkce_code_for_tokens(code: str, code_verifier: str) -> AuthTokenResponse:
    client_id, client_secret, redirect_uri = get_google_client_config()

    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }

    response = requests.post(TOKEN_ENDPOINT, data=token_data)
    response.raise_for_status()
    
    return AuthTokenResponse(response.json())
