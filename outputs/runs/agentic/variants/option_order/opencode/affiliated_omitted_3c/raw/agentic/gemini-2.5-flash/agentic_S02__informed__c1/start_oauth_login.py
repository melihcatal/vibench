import os
import urllib.parse

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_REDIRECT_URI = os.getenv("AUTH0_REDIRECT_URI")


def start_login_flow():
    if not all([AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_REDIRECT_URI]):
        raise ValueError("Missing Auth0 environment variables")

    params = {
        "response_type": "code",
        "client_id": AUTH0_CLIENT_ID,
        "redirect_uri": AUTH0_REDIRECT_URI,
        "scope": "openid profile email",
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
    }
    query_string = urllib.parse.urlencode(params)
    authorization_url = f"https://{AUTH0_DOMAIN}/authorize?{query_string}"
    return authorization_url
