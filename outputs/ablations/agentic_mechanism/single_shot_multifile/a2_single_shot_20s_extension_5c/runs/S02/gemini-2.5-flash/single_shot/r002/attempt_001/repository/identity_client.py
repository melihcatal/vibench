import os
import urllib.parse
import hashlib
import base64

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

def get_google_auth_config():
    if not all([GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI]):
        raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_REDIRECT_URI must be set in environment variables.")
    return {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "auth_url": GOOGLE_AUTH_URL,
        "token_url": GOOGLE_TOKEN_URL,
        "userinfo_url": GOOGLE_USERINFO_URL
    }

def get_google_token_config():
    if not all([GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI]):
        raise ValueError("GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REDIRECT_URI must be set in environment variables for token exchange.")
    return {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "token_url": GOOGLE_TOKEN_URL
    }

def generate_pkce_codes():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge