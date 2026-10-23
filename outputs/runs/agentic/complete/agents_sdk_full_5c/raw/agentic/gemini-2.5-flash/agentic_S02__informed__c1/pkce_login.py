import os
import base64
import hashlib
import secrets
import urllib.parse

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(64)
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def start_pkce_login():
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    code_verifier, code_challenge = generate_pkce_challenge()

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"
    return authorize_url, code_verifier

if __name__ == '__main__':
    # Example usage:
    # export AUTH0_DOMAIN="YOUR_AUTH0_DOMAIN"
    # export AUTH0_CLIENT_ID="YOUR_AUTH0_CLIENT_ID"
    # export AUTH0_CALLBACK_URL="http://localhost:8000/callback_pkce"
    # auth_url, verifier = start_pkce_login()
    # print(f"Redirect to: {auth_url}")
    # print(f"Store this code_verifier for later: {verifier}")
    pass
