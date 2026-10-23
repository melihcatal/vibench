import os
import base64
import hashlib
import webbrowser
import urllib.parse
import requests
from identity_client import AUTH_URL, AUTH0_CLIENT_ID, REDIRECT_URI, TOKEN_URL
from identity_models import OauthToken

def generate_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
    challenge_data = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(challenge_data).decode("utf-8").rstrip("=")
    return verifier, challenge

def start_pkce_login() -> str:
    verifier, challenge = generate_pkce_pair()
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    query = urllib.parse.urlencode(params)
    url = f"{AUTH_URL}?{query}"
    webbrowser.open(url)
    return verifier

def exchange_pkce_code(code: str, verifier: str) -> OauthToken:
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": verifier,
    }
    resp = requests.post(TOKEN_URL, data=data)
    resp.raise_for_status()
    token_data = resp.json()
    return OauthToken(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        id_token=token_data.get("id_token"),
    )