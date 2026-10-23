import os
import urllib.parse


def start_auth0_login():
    """
    Constructs the Auth0 authorization URL to start an OAuth 2.0 / OIDC login flow.
    """
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_CALLBACK_URL = os.environ.get(
        "AUTH0_CALLBACK_URL", "http://localhost:8000/callback"
    )

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
    login_url = start_auth0_login()
    print(f"Please visit this URL to log in: {login_url}")
