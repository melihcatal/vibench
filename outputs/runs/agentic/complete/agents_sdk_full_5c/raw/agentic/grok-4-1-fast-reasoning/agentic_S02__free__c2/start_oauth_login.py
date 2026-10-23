import os
import secrets
from urllib.parse import urlencode
import webbrowser
from identity_client import get_client_config
from identity_models import TokenResponse

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPES = ["openid", "profile", "email"]

def start_oauth_login(redirect_uri: str) -> str:
    config = get_client_config("google")
    state = secrets.token_urlsafe(32)
    params = {
        "client_id": config["client_id"],
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "state": state,
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    print(f"Login URL opened. State: {state}")
    webbrowser.open(auth_url)
    return state