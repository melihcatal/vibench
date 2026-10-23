import os
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, OAuthConfig

def initiate_oauth_login(provider: str, redirect_uri: str, state: str) -> str:
    config: OAuthConfig = get_oauth_config(provider)
    
    auth0_client = OAuth2Session(
        client_id=config.client_id,
        client_secret=config.client_secret,
        scope="openid profile email",
        redirect_uri=redirect_uri,
    )
    
    authorization_url, _ = auth0_client.create_authorization_url(
        url=f"https://{config.domain}/authorize",
        state=state,
        audience=config.audience,
    )
    
    return authorization_url