from authlib.integrations.requests_client import OAuth2Session
import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "https://example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")


def start_auth0_login():
    session = OAuth2Session(
        AUTH0_CLIENT_ID,
        scope="openid profile email",
        redirect_uri=AUTH0_CALLBACK_URL
    )
    authorization_url, state = session.create_authorization_url(
        f"{AUTH0_DOMAIN}/authorize"
    )
    return {
        "authorization_url": authorization_url,
        "state": state,
        "provider": "auth0"
    }