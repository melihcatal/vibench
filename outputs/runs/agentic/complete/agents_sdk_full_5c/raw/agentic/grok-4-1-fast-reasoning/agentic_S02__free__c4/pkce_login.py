import secrets
import hashlib
import base64
import urllib.parse
import webbrowser
import requests
from identity_client import GoogleOAuthConfig
from identity_models import OAuthToken

def generate_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")

def start_pkce_login(scopes: list[str] = ["openid", "profile", "email"]):
    config = GoogleOAuthConfig()
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    challenge = generate_pkce_challenge(verifier)
    state = secrets.token_urlsafe(32)
    params = {
        "response_type": "code",
        "client_id": config.CLIENT_ID,
        "redirect_uri": config.REDIRECT_URI,
        "scope": " ".join(scopes),
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    query_string = urllib.parse.urlencode(params)
    auth_url = f"{config.AUTH_URL}?{query_string}"
    webbrowser.open(auth_url)
    return verifier, state

def pkce_token_exchange(code: str, verifier: str):
    config = GoogleOAuthConfig()
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": config.REDIRECT_URI,
        "client_id": config.CLIENT_ID,
        "code_verifier": verifier,
    }
    response = requests.post(config.TOKEN_URL, data=data)
    response.raise_for_status()
    tokens = response.json()
    return OAuthToken(**tokens)