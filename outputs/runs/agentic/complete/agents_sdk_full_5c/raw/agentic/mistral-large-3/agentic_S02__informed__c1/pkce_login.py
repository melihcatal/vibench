from authlib.integrations.requests_client import OAuth2Session
import os
from secrets import token_urlsafe
from identity_client import get_identity_config


def generate_pkce_login_url(redirect_uri: str) -> tuple[str, str]:
    config = get_identity_config()
    auth0_domain = os.getenv("AUTH0_DOMAIN")
    auth0_client_id = os.getenv("AUTH0_CLIENT_ID")
    authorize_url = f"https://{auth0_domain}/authorize"

    code_verifier = token_urlsafe(32)
    session = OAuth2Session(
        client_id=auth0_client_id,
        scope="openid profile email",
        redirect_uri=redirect_uri
    )
    authorization_url, state = session.create_authorization_url(
        authorize_url, code_verifier=code_verifier
    )
    return authorization_url, code_verifier