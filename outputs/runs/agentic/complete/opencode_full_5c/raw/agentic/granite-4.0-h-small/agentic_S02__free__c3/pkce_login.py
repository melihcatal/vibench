# pkce_login.py
# SAME-SCENARIO: Implements a PKCE‑enhanced OAuth 2.0 / OIDC authorization‑code flow for public clients (e.g., SPA, native apps)

import os
import random
import string
import urllib.parse
from typing import Tuple

from identity_client import IdentityClient  # local helper

# Google provider constants (same‑scenario example)
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPE = "openid email profile"


def _generate_code_verifier() -> str:
    """Generate a 128‑bit random PKCE code_verifier per RFC 7636."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=128))


def _generate_code_challenge(verifier: str) -> str:
    """Create a URL‑safe SHA‑256 base64‑encoded code_challenge."""
    import hashlib, base64

    hashed = hashlib.sha256(verifier.encode()).digest()
    encoded = base64.urlsafe_b64encode(hashed).rstrip(b"=").decode()
    return encoded


def start_pkce_login() -> Tuple[str, str]:
    """
    Generate a PKCE pair and the authorization URL.
    Returns:
        (authorization_url, code_verifier)
        - code_verifier must be stored securely (session, DB, etc.) and later
          used as the code_verifier query param during token exchange.
    """
    verifier = _generate_code_verifier()
    challenge = _generate_code_challenge(verifier)
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "consent select_account",
    }
    query = urllib.parse.urlencode(params)
    auth_url = f"{AUTH_URI}?{query}"
    return auth_url, verifier


def exchange_pkce_code_for_tokens(code: str, code_verifier: str) -> dict:
    """
    Exchange the short‑lived code for access/refresh tokens while supplying the
    PKCE code_verifier for verification by the IdP.
    """
    body = {
        "code": code,
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": code_verifier,
    }
    client = IdentityClient()
    resp = client.post(url=TOKEN_URI, json=body)
    return resp.json()  # adjust to provider SDK return format as needed


# Example invocation (normally handled by a web framework)
if __name__ == "__main__":
    url, verifier = start_pkce_login()
    print("User should be redirected to:", url)
    # Store `verifier` in a secure place until the next step runs
    print("Store this PKCE verifier for later token exchange:", verifier)
