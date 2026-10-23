import os
import urllib.parse
from identity_client import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL

def start_oauth_login():
    """Constructs and returns the Auth0 authorization URL."""
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    }
    return f"{authorize_url}?{urllib.parse.urlencode(params)}"

if __name__ == "__main__":
    login_url = start_oauth_login()
    print(f"Please visit this URL to start the login process: {login_url}")
