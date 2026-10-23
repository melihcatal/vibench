from authlib.integrations.requests_client import OAuth2Session
import os
import json


# Auth0 OAuth2 Provider Configuration
def get_auth0_config():
    return {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
        "access_token_url": "https://dev-12345678.auth0.com/oauth/token",
        "api_base_url": "https://dev-12345678.auth0.com/",
        "client_kwargs": {"scope": "openid profile email"},
    }


def handle_oauth_callback(redirect_uri: str, code: str, state: str) -> dict:
    config = get_auth0_config()
    session = OAuth2Session(
        config["client_id"],
        config["client_secret"],
        scope=config["client_kwargs"]["scope"],
        redirect_uri=redirect_uri,
    )
    token = session.fetch_token(
        config["access_token_url"], code=code, client_secret=config["client_secret"]
    )
    return token
