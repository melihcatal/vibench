
import os
import base64
import hashlib
import json
import requests

# Auth0 Configuration (replace with your actual Auth0 domain and client ID)
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:3000/callback")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")

def generate_code_verifier_and_challenge():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def get_authorization_url(code_challenge: str, state: str) -> str:
    """Constructs the Auth0 authorization URL."""
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "audience": AUTH0_AUDIENCE,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": state,
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{authorize_url}?{query_string}"

def exchange_code_for_tokens(code: str, code_verifier: str) -> dict:
    """Exchanges the authorization code for access, ID, and refresh tokens."""
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
        "code": code,
        "redirect_uri": AUTH0_REDIRECT_URI,
    }
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

