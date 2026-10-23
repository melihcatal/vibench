import os
from authlib.integrations.httpx_client import OAuth2Client
from identity_client import get_identity_config
from identity_models import OAuth2TokenResponse


async def handle_okta_callback(authorization_code: str) -> OAuth2TokenResponse:
    """
    Handles the callback from Okta, exchanging the authorization code for tokens.
    """
    config = get_identity_config()

    client = OAuth2Client(
        client_id=config["okta_client_id"],
        client_secret=config["okta_client_secret"],
        redirect_uri=config["redirect_uri"],
    )

    metadata_url = f"https://{config['okta_domain']}/.well-known/openid-configuration"
    await client.fetch_discovery_info(metadata_url)

    token_data = await client.fetch_token(
        grant_type="authorization_code",
        code=authorization_code,
        redirect_uri=config["redirect_uri"],
    )

    return OAuth2TokenResponse(**token_data)
