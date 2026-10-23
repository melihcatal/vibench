import os
import urllib.parse
from identity_client import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI

def get_google_oauth_login_url(state: str) -> str:
    scopes = [
        "openid",
        "email",
        "profile"
    ]
    scope_string = " ".join(scopes)

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": scope_string,
        "access_type": "offline",
        "prompt": "consent select_account",
        "state": state,
    }

    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{urllib.parse.urlencode(params)}"
