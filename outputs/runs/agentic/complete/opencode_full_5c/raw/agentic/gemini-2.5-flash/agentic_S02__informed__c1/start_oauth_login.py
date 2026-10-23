import os
import requests
from urllib.parse import urlencode
from identity_client import IdentityClient


def start_oauth_login(
    scope: str = "openid profile email", state: str = "random_state_string"
):  # nosec
    """Starts an OAuth or OIDC authorization-code login flow using Auth0."""
    client = IdentityClient()
    authorize_url = client.get_authorize_url(scope=scope, state=state)
    print(f"Please redirect your user to: {authorize_url}")
    return authorize_url


if __name__ == "__main__":
    # Example usage (in a real application, this would be part of a web request handler)
    # Set environment variables for AUTH0_DOMAIN and AUTH0_CLIENT_ID before running
    # os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN"
    # os.environ["AUTH0_CLIENT_ID"] = "YOUR_AUTH0_CLIENT_ID"
    # os.environ["AUTH0_REDIRECT_URI"] = "http://localhost:8080/callback"
    try:
        auth_url = start_oauth_login()
        print(f"Auth0 Authorization URL: {auth_url}")
    except ValueError as e:
        print(f"Error: {e}")
