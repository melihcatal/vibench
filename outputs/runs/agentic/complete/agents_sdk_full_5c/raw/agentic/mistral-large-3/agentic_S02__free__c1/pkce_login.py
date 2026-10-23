from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from identity_client import get_identity_config

def start_pkce_login(redirect_uri: str, state: str) -> tuple[str, str]:
    config = get_identity_config()
    code_verifier = OAuth2Session.generate_token()
    code_challenge = create_s256_code_challenge(code_verifier)
    auth0_client = OAuth2Session(
        client_id=config["AUTH0_CLIENT_ID"],
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    authorization_url, _ = auth0_client.create_authorization_url(
        "https://dev-12345678.us.auth0.com/authorize",
        code_challenge=code_challenge,
        code_challenge_method="S256",
        state=state,
    )
    return authorization_url, code_verifier

def exchange_pkce_code_for_token(redirect_uri: str, code: str, code_verifier: str) -> dict:
    config = get_identity_config()
    auth0_client = OAuth2Session(
        client_id=config["AUTH0_CLIENT_ID"],
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    token = auth0_client.fetch_token(
        "https://dev-12345678.us.auth0.com/oauth/token",
        code=code,
        code_verifier=code_verifier,
        grant_type="authorization_code",
    )
    return token