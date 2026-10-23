from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7636 import create_s256_code_challenge
import os
import uuid


# Auth0 OAuth2 Provider Configuration
def get_auth0_config():
    return {
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
        "authorize_url": "https://dev-12345678.auth0.com/authorize",
        "access_token_url": "https://dev-12345678.auth0.com/oauth/token",
        "api_base_url": "https://dev-12345678.auth0.com/",
        "client_kwargs": {"scope": "openid profile email"},
    }


def start_pkce_login(redirect_uri: str) -> dict:
    config = get_auth0_config()
    code_verifier = uuid.uuid4().hex
    code_challenge = create_s256_code_challenge(code_verifier)
    code_challenge_method = "S256"

    session = OAuth2Session(
        config["client_id"],
        scope=config["client_kwargs"]["scope"],
        redirect_uri=redirect_uri,
    )
    state = str(uuid.uuid4())
    authorization_url, _ = session.create_authorization_url(
        config["authorize_url"],
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        state=state,
    )
    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier,
    }
