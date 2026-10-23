from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7636 import create_s256_code_challenge
import os
import uuid


# Auth0 OAuth2 Provider Configuration
def get_auth0_config():
    return {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "client_secret": os.getenv("AUTH0_CLIENT_SECRET"),
        "authorize_url": "https://dev-12345678.auth0.com/authorize",
        "access_token_url": "https://dev-12345678.auth0.com/oauth/token",
        "api_base_url": "https://dev-12345678.auth0.com/",
        "client_kwargs": {"scope": "openid profile email"},
    }


def start_oauth_login(redirect_uri: str) -> str:
    config = get_auth0_config()
    session = OAuth2Session(
        config["client_id"],
        config["client_secret"],
        scope=config["client_kwargs"]["scope"],
        redirect_uri=redirect_uri,
    )
    state = str(uuid.uuid4())
    authorization_url, _ = session.create_authorization_url(
        config["authorize_url"], state=state
    )
    return authorization_url
