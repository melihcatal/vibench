import os
from urllib.parse import urlencode

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.environ.get("AUTH0_CALLBACK_URL")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")


def get_auth0_authorize_url(redirect_uri: str, state: str, code_challenge: str = None):
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "openid profile email",
        "state": state,
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = "S256"
    return f"https://{AUTH0_DOMAIN}/authorize?{urlencode(params)}"


def get_auth0_token_url():
    return f"https://{AUTH0_DOMAIN}/oauth/token"


def get_auth0_userinfo_url():
    return f"https://{AUTH0_DOMAIN}/userinfo"
