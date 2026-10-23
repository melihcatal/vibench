import os
import urllib.parse
from typing import Optional

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPES = "openid profile email"


def start_oauth_login(redirect_uri: str, state: Optional[str] = None) -> str:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": SCOPES,
        "response_type": "code",
        "access_type": "offline",
    }
    if state:
        params["state"] = state
    query_string = urllib.parse.urlencode(params)
    return f"{GOOGLE_AUTH_URL}?{query_string}"
