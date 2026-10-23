import os
import hashlib
import base64
from typing import Tuple
from urllib.parse import urlencode
import requests

# Google Identity Platform OIDC
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
GOOGLE_SCOPES = ["openid", "profile", "email"]


def generate_pkce_pair() -> Tuple[str, str]:
    """Generate PKCE code verifier and challenge."""
    verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )
    return verifier, challenge


def pkce_login(state: str) -> Tuple[str, str]:
    # Generate PKCE pair
    code_verifier, code_challenge = generate_pkce_pair()

    # Fetch Google's OIDC configuration
    discovery_doc = requests.get(GOOGLE_DISCOVERY_URL).json()
    auth_endpoint = discovery_doc["authorization_endpoint"]

    # Build the authorization request with PKCE
    params = {
        "client_id": GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": " ".join(GOOGLE_SCOPES),
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    auth_url = f"{auth_endpoint}?{urlencode(params)}"
    return auth_url, code_verifier
