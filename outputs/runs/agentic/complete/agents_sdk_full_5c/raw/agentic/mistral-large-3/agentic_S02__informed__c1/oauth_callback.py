from authlib.integrations.requests_client import OAuth2Session
import os
from identity_client import get_identity_config
from identity_models import TokenResponse


def handle_oauth_callback(redirect_uri: str, code: str) -> TokenResponse:
    config = get_identity_config()
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
    auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    token_url = f"https://{auth0_domain}/oauth/token"

    session = OAuth2Session(
        client_id=auth0_client_id,
        client_secret=auth0_client_secret,
        scope="openid profile email",
        redirect_uri=redirect_uri
    )
    token = session.fetch_token(token_url, code=code, grant_type="authorization_code")
    return TokenResponse(**token)