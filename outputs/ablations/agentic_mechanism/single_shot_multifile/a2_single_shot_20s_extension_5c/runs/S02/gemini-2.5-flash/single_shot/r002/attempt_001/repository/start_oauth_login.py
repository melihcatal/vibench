import os
import urllib.parse
from identity_client import get_google_auth_config

def start_google_oauth_login(scopes: list[str], state: str) -> str:
    config = get_google_auth_config()
    params = {
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "state": state
    }
    authorization_url = f"{config['auth_url']}?{urllib.parse.urlencode(params)}"
    return authorization_url