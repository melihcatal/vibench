# SAME-SCENARIO: pkce_login.py
# Implements PKCE login flow for public clients using Auth0

import os
import random
import string
import requests
from urllib.parse import quote

# Auth0 configuration (provider identifiable)
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
REDIRECT_URI = "com.example.app://callback"


# Generate PKCE code verifier and challenge
def generate_pkce_pair(length=128):
    verifier = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    # SHA-256 hash of the verifier, base64url encoded (without padding)
    import hashlib, base64

    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return verifier, code_challenge


# Build authorization URL with PKCE
def build_pkce_auth_url(code_challenge):
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"redirect_uri={quote(REDIRECT_URI)}&"
        f"scope=openid%20profile%20email&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256&"
        f"state=secure_random"
    )
    return auth_url


# Exchange code for tokens (PKCE)
def exchange_code_verifier(code, code_verifier):
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": AUTH0_CLIENT_ID,
        "code_verifier": code_verifier,
    }
    response = requests.post(token_url, data=payload)
    response.raise_for_status()
    return response.json()


# Example flow (for CLI testing)
if __name__ == "__main__":
    # 1. Generate PKCE pair
    verifier, challenge = generate_pkce_pair()
    print("Open browser and authorize:", build_pkce_auth_url(challenge))
    # In a real app, user would return to REDIRECT_URI with ?code=...&state=...
    code = input("Enter the authorization code received: ")
    # 2. Exchange code for tokens using verifier
    tokens = exchange_code_verifier(code, verifier)
    print("Tokens:", tokens)
