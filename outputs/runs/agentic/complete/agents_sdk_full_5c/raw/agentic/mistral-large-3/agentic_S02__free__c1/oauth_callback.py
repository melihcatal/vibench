from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_identity_config

def exchange_code_for_token(redirect_uri: str, code: str) -> dict:
    config = get_identity_config()
    auth0_client = OAuth2Session(
        client_id=config["AUTH0_CLIENT_ID"],
        client_secret=config["AUTH0_CLIENT_SECRET"],
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    token = auth0_client.fetch_token(
        "https://dev-12345678.us.auth0.com/oauth/token",
        code=code,
        grant_type="authorization_code",
    )
    return token