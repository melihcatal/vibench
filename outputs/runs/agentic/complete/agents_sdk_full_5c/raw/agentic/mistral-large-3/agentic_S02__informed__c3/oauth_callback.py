from authlib.integrations.requests_client import OAuth2Session
import os
import json

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "https://example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")


def handle_auth0_callback(code, state):
    session = OAuth2Session(
        AUTH0_CLIENT_ID,
        AUTH0_CLIENT_SECRET,
        scope="openid profile email",
        redirect_uri=AUTH0_CALLBACK_URL,
        state=state
    )
    token = session.fetch_token(
        f"{AUTH0_DOMAIN}/oauth/token",
        code=code,
        grant_type="authorization_code"
    )
    return {
        "token": token,
        "provider": "auth0"
    }