import os
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, OAuthConfig
from identity_models import TokenResponse


def exchange_code_for_tokens(provider: str, redirect_uri: str, code: str) -> TokenResponse:
    config: OAuthConfig = get_oauth_config(provider)
    
    auth0_client = OAuth2Session(
        client_id=config.client_id,
        client_secret=config.client_secret,
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    
    token_response = auth0_client.fetch_token(
        url=f"https://{config.domain}/oauth/token",
        code=code,
        grant_type="authorization_code",
    )
    
    return TokenResponse(
        access_token=token_response["access_token"],
        id_token=token_response["id_token"],
        refresh_token=token_response.get("refresh_token"),
        expires_in=token_response["expires_in"],
    )