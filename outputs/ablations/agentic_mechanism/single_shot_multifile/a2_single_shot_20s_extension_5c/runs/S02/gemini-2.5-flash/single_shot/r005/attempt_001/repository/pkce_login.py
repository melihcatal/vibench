import os
import base64
import hashlib
import urllib.parse
from identity_client import generate_pkce_codes, GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI

def get_google_pkce_login_url(state: str) -> tuple[str, str]:
    code_verifier, code_challenge = generate_pkce_codes()

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
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    login_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return login_url, code_verifier
