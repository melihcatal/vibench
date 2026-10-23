import os
import requests
from identity_models import TokenExchangeRequest, TokenExchangeResponse
from identity_client import get_oauth_config

def exchange_code_for_tokens(token_exchange_request: TokenExchangeRequest) -> TokenExchangeResponse:
    """Exchanges an authorization code for access and ID tokens with Google OAuth2."""
    config = get_oauth_config("google")

    token_url = config["token_uri"]
    data = {
        "code": token_exchange_request.code,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "redirect_uri": config["redirect_uri"],
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    token_data = response.json()

    return TokenExchangeResponse(
        access_token=token_data["access_token"],
        id_token=token_data["id_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        refresh_token=token_data.get("refresh_token"),
    )

def oauth_callback(code: str, redirect_uri: str):
    """Handles the OAuth callback and initiates token exchange."""
    token_request = TokenExchangeRequest(
        code=code,
        redirect_uri=redirect_uri,
        client_id=os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID"),
        client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET"),
    )
    token_response = exchange_code_for_tokens(token_request)
    return token_response
