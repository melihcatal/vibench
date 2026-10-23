import os
import sys
import random
import string
import hmac
import base64
import hashlib
from urllib.parse import urlencode
from identity_client import IdentityClient

# IBM App ID PKCE configuration (can be adapted for any provider)
IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
REDIRECT_URI = "http://localhost:5000/oauth/callback"
TOKEN_ENDPOINT = "https://us-south.appid.cloud.ibm.com/oauth/v4/token"


def generate_code_verifier() -> str:
    """Generate a PKCE code verifier (high-entropy string)."""
    code_verifier = "".join(
        random.SystemRandom().choice(string.ascii_letters + string.digits)
        for _ in range(128)
    )
    return code_verifier


def generate_code_challenge(verifier: str) -> str:
    """Create a URL-safe base64-encoded SHA-256 hash of the verifier."""
    hash_bytes = hashlib.sha256(verifier.encode()).digest()
    # URL-safe base64 without padding, as required by OAuth 2.0 PKCE
    challenge = base64.urlsafe_b64encode(hash_bytes).decode().rstrip("=")
    return challenge


def pkce_login():
    """Implement the PKCE login flow for public clients.

    Returns:
        dict: Authorization endpoint URL and generated PKCE values for client use.
    """
    client = IdentityClient(
        base_url=None,  # No token endpoint needed here
        client_id=IBM_APPID_CLIENT_ID,
        client_secret=None,  # Public client; secret not used
    )

    # 1. Generate verifier and challenge
    code_verifier = generate_code_verifier()
    code_challenge = generate_code_challenge(code_verifier)

    # 2. Build authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": IBM_APPID_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
        # Optional: include additional scopes or state for CSRF protection
        # 'state': client.generate_state(),
    }
    auth_url = f"https://us-south.appid.cloud.ibm.com/oauth/v4/authorize?{urlencode(auth_params)}"
    return {
        "auth_url": auth_url,
        "code_verifier": code_verifier,  # Store securely to verify later when exchanging code
    }


if __name__ == "__main__":
    # Local demo: print the auth URL and store verifier (for demo only!)
    result = pkce_login()
    print("Redirect the user to this URL:")
    print(result["auth_url"])
    # In a real app you'd store the verifier (e.g. in an HTTP session) for later exchange
