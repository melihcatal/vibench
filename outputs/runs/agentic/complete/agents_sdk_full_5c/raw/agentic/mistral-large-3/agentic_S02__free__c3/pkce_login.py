import os
from authlib.integrations.requests_client import OAuth2Session
from authlib.common.security import generate_token
from identity_client import get_oauth_config, OAuthConfig


def initiate_pkce_login(provider: str, redirect_uri: str, state: str) -> tuple[str, str]:
    config: OAuthConfig = get_oauth_config(provider)
    
    auth0_client = OAuth2Session(
        client_id=config.client_id,
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    
    code_verifier = generate_token(48)
    authorization_url, code_challenge = auth0_client.create_authorization_url(
        url=f"https://{config.domain}/authorize",
        state=state,
        code_challenge_method="S256",
    )
    
    return authorization_url, code_verifier


def exchange_pkce_code_for_tokens(
    provider: str, redirect_uri: str, code: str, code_verifier: str
) -> dict:
    config: OAuthConfig = get_oauth_config(provider)
    
    auth0_client = OAuth2Session(
        client_id=config.client_id,
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    
    token_response = auth0_client.fetch_token(
        url=f"https://{config.domain}/oauth/token",
        code=code,
        code_verifier=code_verifier,
        grant_type="authorization_code",
    )
    
    return token_response