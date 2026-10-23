import os
import urllib.parse
from identity_client import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI

def start_google_oauth_login():
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account"
    }
    return f"{auth_url}?{urllib.parse.urlencode(params)}"
