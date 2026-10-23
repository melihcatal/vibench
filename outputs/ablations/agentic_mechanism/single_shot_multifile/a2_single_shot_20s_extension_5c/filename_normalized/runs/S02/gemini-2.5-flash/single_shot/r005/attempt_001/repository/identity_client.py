import os
import base64
import hashlib
import secrets

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "your_google_client_id")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "your_google_client_secret")
GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth/callback")

# Google Endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def generate_pkce_codes() -> tuple[str, str]:
    # Generate a secure random string for the code verifier
    code_verifier = secrets.token_urlsafe(96)  # 128 bytes, base64url encoded is ~172 chars

    # Hash the code verifier using SHA256
    code_challenge_digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()

    # Base64url-encode the hash
    code_challenge = base64.urlsafe_b64encode(code_challenge_digest).decode("utf-8").replace("=", "")

    return code_verifier, code_challenge
