import os
import urllib.parse

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

def start_auth0_login():
    """Starts an Auth0 OAuth 2.0 Authorization Code Grant flow."""
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 environment variables.")

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
    print(f"Redirect to: {login_url}")
