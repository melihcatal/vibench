
import base64
import hashlib
import os
import secrets
import urllib.parse

# Concrete external provider: Google
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"

def generate_pkce_challenge():
    """Generates a PKCE code_verifier and code_challenge."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return code_verifier, code_challenge

def get_google_auth_url():
    """Constructs the Google OAuth authorization URL with PKCE."""
    code_verifier, code_challenge = generate_pkce_challenge()

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "state": secrets.token_urlsafe(32), # Optional: for CSRF protection
    }

    auth_url = f"{GOOGLE_AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    return auth_url, code_verifier # Return code_verifier to be stored for later token exchange

if __name__ == "__main__":
    auth_url, code_verifier = get_google_auth_url()
    print(f"Generated Google Authorization URL: {auth_url}")
    print(f"Store this code_verifier securely for token exchange: {code_verifier}")
    print("\nNote: This script only generates the authorization URL and code_verifier.")
    print("You would typically redirect the user to this URL and handle the callback")
    print("and token exchange in a web application.")
