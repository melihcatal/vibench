import os
import base64
import hashlib
import urllib.parse

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")
GOOGLE_AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def generate_pkce_codes():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def start_google_pkce_login(code_challenge: str):
    if not GOOGLE_CLIENT_ID or not GOOGLE_REDIRECT_URI:
        raise ValueError("Google client ID and redirect URI must be set in environment variables.")

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"{GOOGLE_AUTHORIZATION_BASE_URL}?{urllib.parse.urlencode(params)}"

def exchange_pkce_code_for_tokens(authorization_code: str, code_verifier: str):
    import requests # Imported locally to avoid circular dependencies if this was a shared helper

    if not GOOGLE_CLIENT_ID or not GOOGLE_REDIRECT_URI:
        raise ValueError("Google client ID and redirect URI must be set in environment variables.")

    data = {
        "code": authorization_code,
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(GOOGLE_TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    return response.json()
