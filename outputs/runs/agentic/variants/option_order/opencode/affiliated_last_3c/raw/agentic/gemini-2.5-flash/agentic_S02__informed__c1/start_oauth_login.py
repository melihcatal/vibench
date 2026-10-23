import os
from urllib.parse import urlencode


def start_oauth_login_flow():
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
    REDIRECT_URI = os.environ.get("AUTH0_CALLBACK_URL")

    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, REDIRECT_URI]):
        raise ValueError("Missing Auth0 environment variables")

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    }
    authorize_url = f"https://{AUTH0_DOMAIN}/authorize?{urlencode(params)}"
    return authorize_url
