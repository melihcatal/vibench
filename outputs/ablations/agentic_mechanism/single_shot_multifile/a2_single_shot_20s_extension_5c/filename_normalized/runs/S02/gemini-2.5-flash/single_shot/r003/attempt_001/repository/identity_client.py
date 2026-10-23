import os
import base64
import hashlib
import secrets

# Google OAuth2/OIDC Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/google/callback")

# Auth0 PKCE Configuration
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8000/auth0/callback")

def generate_pkce_verifier(length: int = 128) -> str:
    return secrets.token_urlsafe(length)

def generate_pkce_challenge(verifier: str) -> str:
    s256 = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')
