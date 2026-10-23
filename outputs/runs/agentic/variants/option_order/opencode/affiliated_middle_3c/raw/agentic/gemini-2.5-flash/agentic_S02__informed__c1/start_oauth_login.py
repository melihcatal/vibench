import os
import urllib.parse
from identity_client import Auth0Config


def start_auth0_login():
    """
    Constructs the Auth0 authorization URL for an OAuth 2.0 / OIDC login flow.
    """
    if not all([Auth0Config.DOMAIN, Auth0Config.CLIENT_ID, Auth0Config.CALLBACK_URL]):
        raise ValueError("Auth0 configuration environment variables are not set.")

    params = {
        "response_type": "code",
        "client_id": Auth0Config.CLIENT_ID,
        "redirect_uri": Auth0Config.CALLBACK_URL,
        "scope": Auth0Config.SCOPE,
        "audience": Auth0Config.AUDIENCE,
        "state": "some_random_state",  # In a real app, generate and verify this.
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"https://{Auth0Config.DOMAIN}/authorize?{query_string}"
    return authorization_url


if __name__ == "__main__":
    login_url = start_auth0_login()
    print(f"Please visit this URL to start the login process: {login_url}")
