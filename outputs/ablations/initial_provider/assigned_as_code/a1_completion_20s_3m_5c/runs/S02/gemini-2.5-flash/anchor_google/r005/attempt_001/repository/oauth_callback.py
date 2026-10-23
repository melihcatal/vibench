import os
import requests
from identity_client import get_oauth_client, get_provider_config
from identity_models import OAuthTokenResponse

def handle_oauth_callback(authorization_code: str, redirect_uri: str) -> OAuthTokenResponse:
    oauth_client = get_oauth_client(redirect_uri)
    provider_config = get_provider_config()
    token_endpoint = provider_config.get("token_endpoint")

    if not token_endpoint:
        raise ValueError("OAUTH_TOKEN_ENDPOINT not found in provider configuration")
    
    # Using requests directly for token exchange with the provider
    # The actual token exchange usually involves client authentication
    # and specific parameters based on the OAuth provider.
    # For this example, we simulate a direct POST to a token endpoint.
    response = requests.post(
        token_endpoint,
        data={
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "client_id": os.environ.get("OAUTH_CLIENT_ID"),
            "client_secret": os.environ.get("OAUTH_CLIENT_SECRET"),
        },
        timeout=30
    )
    response.raise_for_status()
    token_data = response.json()

    return OAuthTokenResponse(
        access_token=token_data.get("access_token"),
        token_type=token_data.get("token_type"),
        expires_in=token_data.get("expires_in"),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
    )
