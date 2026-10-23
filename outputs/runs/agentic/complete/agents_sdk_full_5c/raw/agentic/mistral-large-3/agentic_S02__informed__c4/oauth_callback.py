import os
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oidc_config

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


def handle_oauth_callback(code, state):
    oidc_config = get_oidc_config(f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration")
    token_endpoint = oidc_config["token_endpoint"]
    session = OAuth2Session(
        AUTH0_CLIENT_ID, 
        AUTH0_CLIENT_SECRET, 
        scope="openid profile email", 
        redirect_uri=AUTH0_CALLBACK_URL
    )
    token = session.fetch_token(token_endpoint, code=code, state=state)
    return {
        "access_token": token["access_token"],
        "id_token": token["id_token"],
        "refresh_token": token.get("refresh_token"),
        "expires_in": token["expires_in"],
        "provider": "auth0"
    }