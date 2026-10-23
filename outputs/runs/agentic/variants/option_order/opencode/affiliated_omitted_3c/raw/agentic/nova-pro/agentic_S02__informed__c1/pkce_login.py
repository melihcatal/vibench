import os
import requests
import hashlib
import secrets

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")


def pkce_login():
    code_verifier = secrets.token_urlsafe(96)
    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = (
        base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode("utf-8")
    )
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:3000/callback",
        "scope": "openid profile email",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    response = requests.get(auth_url, params=params)
    return response.url, code_verifier
