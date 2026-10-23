import os
import requests
from identity_client import IdentityClient

def start_oauth_login(redirect_uri, scope="openid email"):
    client = IdentityClient()
    # Auth0 configuration
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    # Build authorization URL
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": "random-state",
        "nonce": "random-nonce"
    }
    auth_url = f"https://{AUTH0_DOMAIN}/authorize?" + requests.compat.urlencode(params)
    print("Redirect user to:", auth_url)
    # In a real app you would redirect the user's browser to auth_url

if __name__ == "__main__":
    # Example usage – replace with your own callback endpoint
    start_oauth_login("https://example.com/callback")
