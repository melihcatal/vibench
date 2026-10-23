import os
from authlib.integrations.requests_client import OAuth2Session
from authlib.oauth2.rfc7636 import create_s256_code_challenge
from identity_client import get_oauth_config, OAuthConfig


def start_pkce_login(provider: str, redirect_uri: str, state: str) -> tuple[str, str]:
    config: OAuthConfig = get_oauth_config(provider)
    
    auth0_client = OAuth2Session(
        client_id=config.client_id,
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    
    code_verifier = auth0_client.generate_token()[1]
    code_challenge = create_s256_code_challenge(code_verifier)
    
    authorization_url, _ = auth0_client.create_authorization_url(
        url=config.authorize_url,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
        audience=config.audience,
    )
    
    return authorization_url, code_verifier


def exchange_pkce_code_for_tokens(provider: str, redirect_uri: str, code: str, code_verifier: str) -> dict:
    config: OAuthConfig = get_oauth_config(provider)
    
    auth0_client = OAuth2Session(
        client_id=config.client_id,
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    
    token = auth0_client.fetch_token(
        url=config.token_url,
        code=code,
        code_verifier=code_verifier,
        grant_type="authorization_code",
    )
    
    return token