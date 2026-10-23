# start_oauth_login.py
# SAME-SCENARIO: Starts an OAuth 2.0 / OIDC Authorization Code login flow using Google Identity Platform

import os
import urllib.parse

from identity_client import IdentityClient  # local helper

# Google provider constants
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
OAUTH_TOKEN_URI = "https://oauth2.googleapis.com/token"
SCOPE = "openid email profile"


def start_login(state: str, nonce: str) -> str:
    """Generate the authorization URL for the user.

    Args:
        state: CSRF protection opaque value.
        nonce: Random value stored by the client for later verification.
    Returns:
        A URL the user should be redirected to.
    """
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "state": state,
        "nonce": nonce,
        "prompt": "consent select_account",
    }
    query = urllib.parse.urlencode(params)
    auth_url = f"{AUTH_URI}?{query}"
    return auth_url


if __name__ == "__main__":
    # Example usage – in production this would be called from a web framework
    state = "random_state_123"
    nonce = "random_nonce_456"
    url = start_login(state, nonce)
    print("Redirect user to:\n", url)
