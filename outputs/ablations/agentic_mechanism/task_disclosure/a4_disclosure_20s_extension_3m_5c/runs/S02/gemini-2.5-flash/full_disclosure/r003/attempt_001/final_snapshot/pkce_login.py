import os
import base64
import hashlib
import requests
import urllib.parse

# Google OAuth 2.0 Endpoints and Configuration
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID") # For public clients, this is often embedded or managed client-side.
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET") # Not strictly needed for public clients with PKCE, but included for completeness.


def generate_code_verifier() -> str:
    """Generates a high-entropy cryptographically random string as a code verifier."""
    return base64.urlsafe_b64encode(os.urandom(32)).rstrip(b"=").decode("utf-8")

def generate_code_challenge(verifier: str) -> str:
    """Generates a code challenge from the code verifier using S256."""
    sha256_hash = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(sha256_hash).rstrip(b"=").decode("utf-8")

def start_pkce_login_flow(scopes: list[str]) -> tuple[str, str]:
    """
    Initiates the PKCE login flow by generating a code verifier and challenge,
    then constructing the authorization URL.

    Args:
        scopes: A list of OAuth scopes to request.

    Returns:
        A tuple containing (authorization_url, code_verifier).
    """
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    scope_string = " ".join(scopes)

    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": scope_string,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",  # To get a refresh token
        "prompt": "consent",       # To ensure consent screen is shown
    }

    authorization_url = f"{GOOGLE_AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    return authorization_url, code_verifier

def exchange_code_for_tokens(authorization_code: str, code_verifier: str) -> dict:
    """
    Exchanges the authorization code for access and ID tokens using the code verifier.

    Args:
        authorization_code: The authorization code received from the OAuth provider.
        code_verifier: The original code verifier used to start the flow.

    Returns:
        A dictionary containing the token response from the OAuth provider.
    """
    token_params = {
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "code": authorization_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }
    # For public clients, the client_secret is typically not sent in the token exchange.
    # However, if it were a confidential client, it would be included:
    # token_params["client_secret"] = GOOGLE_CLIENT_SECRET

    response = requests.post(GOOGLE_TOKEN_URL, data=token_params)
    response.raise_for_status()
    return response.json()

