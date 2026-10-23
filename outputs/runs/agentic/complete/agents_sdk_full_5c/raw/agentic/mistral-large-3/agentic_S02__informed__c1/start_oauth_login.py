from authlib.integrations.requests_client import OAuth2Session
import os
from identity_client import get_identity_config

def start_oauth_login(redirect_uri: str) -> str:
    config = get_identity_config()
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
    authorize_url = f"https://{auth0_domain}/authorize"

    session = OAuth2Session(
        client_id=auth0_client_id,
        scope="openid profile email",
        redirect_uri=redirect_uri
    )
    authorization_url, state = session.create_authorization_url(authorize_url)
    return authorization_url