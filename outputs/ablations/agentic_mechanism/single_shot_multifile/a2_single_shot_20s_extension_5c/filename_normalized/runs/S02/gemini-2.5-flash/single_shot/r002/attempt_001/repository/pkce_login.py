import os
import requests
import urllib.parse
from identity_client import get_google_auth_config, get_google_token_config, generate_pkce_codes

def start_google_pkce_login(scopes: list[str], state: str) -> tuple[str, str]:
    config = get_google_auth_config()
    code_verifier, code_challenge = generate_pkce_codes()
    
    params = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    }
    authorization_url = f"{config['auth_url']}?{urllib.parse.urlencode(params)}"
    return authorization_url, code_verifier

def handle_google_pkce_callback(authorization_code: str, code_verifier: str) -> dict:
    config = get_google_token_config()
    token_url = config["token_url"]
    token_data = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "code": authorization_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code"
    }
    if "client_secret" in config and config["client_secret"]:
        token_data["client_secret"] = config["client_secret"]

    try:
        response = requests.post(token_url, data=token_data)
        response.raise_for_status()
        tokens = response.json()
        return tokens
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to exchange PKCE authorization code for tokens: {e}")