import os
import sys
import requests
from identity_client import IdentityClient

# Constants for IBM App ID
IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")
AUTHORIZATION_ENDPOINT = "https://us-south.appid.cloud.ibm.com/oauth/v4/authorize"
REDIRECT_URI = "http://localhost:5000/oauth/callback"


def start_oauth_login(state=None, nonce=None):
    """Redirect user to IBM App ID authorization endpoint.

    Args:
        state (str, optional): CSRF protection string.
        nonce (str, optional): Value stored for later token verification.
    """
    client = IdentityClient(
        base_url=AUTHORIZATION_ENDPOINT,
        client_id=IBM_APPID_CLIENT_ID,
        client_secret=IBM_APPID_CLIENT_SECRET,
    )
    params = {
        "response_type": "code",
        "client_id": IBM_APPID_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "state": state or client.generate_state(),
        "nonce": nonce or client.generate_state(),
        # Required for public clients (PKCE)
        "code_challenge_method": "S256",
        # code_challenge will be set later in pkce_login flow
    }
    # Construct full URL (IBM App ID expects querystring)
    url = f"{AUTHORIZATION_ENDPOINT}?{requests.compat.urlencode(params)}"
    print("Redirect user to:")
    print(url)
    # In a real web app you would return an HTTP redirect (302) here.


if __name__ == "__main__":
    # Example usage: python start_oauth_login.py
    start_oauth_login()
