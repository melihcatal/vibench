import os
import urllib.parse
from identity_client import AUTHORIZATION_ENDPOINT, get_google_client_config

def start_google_oauth_login(state: str, scope: str = "openid email profile") -> str:
    client_id, _, redirect_uri = get_google_client_config()

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
        "access_type": "offline",
        "prompt": "select_account"
    }
    
    auth_url = f"{AUTHORIZATION_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return auth_url
