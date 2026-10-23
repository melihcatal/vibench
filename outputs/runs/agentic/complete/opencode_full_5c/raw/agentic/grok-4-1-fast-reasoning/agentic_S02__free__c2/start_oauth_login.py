import os
import secrets
from urllib.parse import urlencode
from identity_client import generate_pkce_pair

GOOGLE_AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")
SCOPES = ["openid", "profile", "email"]


def start_oauth_login(state: str = None) -> tuple[str, str, str]:
    if state is None:
        state = secrets.token_urlsafe(32)
    verifier, challenge = generate_pkce_pair()
    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    auth_url = f"{GOOGLE_AUTHORIZE_URL}?{urlencode(params)}"
    return auth_url, state, verifier
