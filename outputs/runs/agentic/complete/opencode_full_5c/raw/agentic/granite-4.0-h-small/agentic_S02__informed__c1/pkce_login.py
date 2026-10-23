import os
import random
import string
from hashlib import sha256
from base64 import urlsafe_b64encode
from identity_client import IdentityClient


def create_pkce_verifier_and_challenge(length: int = 128) -> tuple[str, str]:
    """Generate a PKCE (Proof Key for Code Exchange) verifier and its SHA-256 challenge.

    length: desired length of the random verifier string (max 128 per spec).
    Returns a tuple (verifier, challenge) where challenge is base64url-encoded SHA-256.
    """
    verifier = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    digest = sha256(verifier.encode()).digest()
    challenge = urlsafe_b64encode(digest).decode().rstrip("=")
    return verifier, challenge


def start_pkce_oauth_flow(
    client_id: str, redirect_uri: str, scopes: list, length: int = 128
):
    """Initiate an OAuth flow using PKCE for public clients.

    Returns a dict with authorization URL and generated PKCE pair.
    """
    verifier, challenge = create_pkce_verifier_and_challenge(length)
    auth_uri = os.getenv(
        "GOOGLE_AUTH_URI",
        "https://accounts.google.com/o/oauth2/v2/auth",
    )
    params = [
        ("client_id", client_id),
        ("redirect_uri", redirect_uri),
        ("response_type", "code"),
        ("scope", " ".join(scopes)),
        ("access_type", "offline"),
        ("prompt", "consent"),
        ("code_challenge", challenge),
        ("code_challenge_method", "S256"),
    ]
    qs = "&".join([f"{k}={v}" for k, v in params])
    url = f"{auth_uri}?{qs}"
    return {"url": url, "verifier": verifier, "challenge": challenge}


# Example usage (web framework route)
# flow = start_pkce_oauth_flow(os.getenv('GOOGLE_CLIENT_ID'), 'https://myapp.example.com/callback', ['openid', 'profile', 'email'])
# print(flow['url'])  # redirect user to this URL
# store flow['verifier'] securely until callback arrives
