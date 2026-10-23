from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_identity_config

def start_oauth_login(redirect_uri: str, state: str) -> str:
    config = get_identity_config()
    auth0_client = OAuth2Session(
        client_id=config["AUTH0_CLIENT_ID"],
        client_secret=config["AUTH0_CLIENT_SECRET"],
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    authorization_url, _ = auth0_client.create_authorization_url(
        "https://dev-12345678.us.auth0.com/authorize",
        state=state,
    )
    return authorization_url