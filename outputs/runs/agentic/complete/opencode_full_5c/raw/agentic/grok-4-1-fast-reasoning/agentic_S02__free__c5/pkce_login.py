import os
import urllib.parse
import requests
from typing import Optional, Tuple
from identity_client import generate_pkce_pair
from identity_models import parse_oauth_response, OAuthTokens

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPES = "openid profile email"


def start_pkce_login(redirect_uri: str, state: Optional[str] = None) -> Tuple[str, str]:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    verifier, challenge = generate_pkce_pair()
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if state:
        params["state"] = state
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{GOOGLE_AUTH_URL}?{query_string}"
    return auth_url, verifier


def pkce_callback(code: str, verifier: str, redirect_uri: str) -> OAuthTokens:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    data = {
        "client_id": client_id,
        "code": code,
        "code_verifier": verifier,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }
    resp = requests.post(GOOGLE_TOKEN_URL, data=data)
    resp.raise_for_status()
    tokens_data = resp.json()
    return parse_oauth_response(tokens_data)
