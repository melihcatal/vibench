import os
import urllib.parse

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")

def start_login():
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CALLBACK_URL]):
        raise ValueError("Missing Auth0 configuration environment variables.")

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_CALLBACK_URL,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    }
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?{urllib.parse.urlencode(params)}"
    return authorize_url

if __name__ == '__main__':
    # Example usage:
    # Set environment variables:
    # export AUTH0_DOMAIN="YOUR_AUTH0_DOMAIN"
    # export AUTH0_CLIENT_ID="YOUR_AUTH0_CLIENT_ID"
    # export AUTH0_CALLBACK_URL="http://localhost:8000/callback"
    print(f"Redirect to: {start_login()}")
