import os
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oidc_config

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


def start_oauth_login():
    oidc_config = get_oidc_config(f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration")
    auth_url = oidc_config["authorization_endpoint"]
    session = OAuth2Session(AUTH0_CLIENT_ID, scope="openid profile email", redirect_uri=AUTH0_CALLBACK_URL)
    authorization_url, state = session.create_authorization_url(auth_url)
    return {
        "authorization_url": authorization_url,
        "state": state,
        "provider": "auth0"
    }