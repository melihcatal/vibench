import os
import base64
import hashlib
import requests
from urllib.parse import urlencode

# Google Identity Platform OIDC
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

def generate_pkce_code_verifier() -> str:
    return base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")

def generate_pkce_code_challenge(verifier: str) -> str:
    sha256 = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256).decode("utf-8").rstrip("=")

def start_pkce_login(state: str, code_verifier: str) -> str:
    code_challenge = generate_pkce_code_challenge(code_verifier)
    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "state": state,
        "scope": "openid profile email",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    return auth_url