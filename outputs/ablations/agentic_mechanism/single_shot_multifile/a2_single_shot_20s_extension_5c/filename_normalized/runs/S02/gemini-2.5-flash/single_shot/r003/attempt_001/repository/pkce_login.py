import os
import requests
import urllib.parse
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI, generate_pkce_challenge, generate_pkce_verifier
from identity_models import TokenResponse

def start_auth0_pkce_login() -> (str, str):
    verifier = generate_pkce_verifier()
    challenge = generate_pkce_challenge(verifier)
    
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    login_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return login_url, verifier

def handle_auth0_pkce_callback(auth_code: str, verifier: str) -> TokenResponse:
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": auth_code,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "code_verifier": verifier,
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()
    return TokenResponse(
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in")
    )
