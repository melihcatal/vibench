import os
import json
import urllib.parse
import requests
from requests.exceptions import RequestException

# Auth0 Hosted Login Page Federation
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


# Auth0 supports PKCE flow for public/native clients
def build_pkce_challenge(verifier_length=128):
    """Generate PKCE code challenge and verifier per RFC 7636.
    Returns:
        tuple: (verifier, challenge)
    """
    import base64, hashlib

    verifier = (
        base64.urlsafe_b64encode(os.urandom(verifier_length))
        .rstrip(b"=")
        .decode("utf-8")
    )
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .rstrip(b"=")
        .decode("utf-8")
    )
    return verifier, challenge


def start_pkce_login(redirect_uri, scope="openid email profile"):
    """Build the PKCE-enabled authorization URL for Auth0.
    Args:
        redirect_uri (str): Your app's callback URL.
        scope (str): OAuth scopes.
    Returns:
        dict: Contains authorization URL and PKCE verifier for storage.
    """
    verifier, challenge = build_pkce_challenge()
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "prompt": "consent",
    }
    query = urllib.parse.urlencode(params)
    login_url = f"https://{AUTH0_DOMAIN}/authorize?" + query
    return {
        "login_url": login_url,
        "pkce_verifier": verifier,
    }


# Example (for local test, prints URLs, store verifier securely):
# result = start_pkce_login('https://myapp.example.com/callback')
# print(result['login_url'])
