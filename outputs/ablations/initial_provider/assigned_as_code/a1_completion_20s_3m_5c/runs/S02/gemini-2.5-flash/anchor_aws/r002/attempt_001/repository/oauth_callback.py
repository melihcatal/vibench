import os
import requests
from urllib.parse import urlencode

from identity_models import OAuthCallbackPayload, TokenExchangeResponse, FederatedLoginConfig
from identity_client import load_federated_login_config

def handle_oauth_callback(payload: OAuthCallbackPayload) -> TokenExchangeResponse:
    config: FederatedLoginConfig = load_federated_login_config()

    # Auth0 specific token endpoint
    token_url = f"https://{config.domain}/oauth/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "client_secret": config.client_secret,
        "code": payload.code,
        "redirect_uri": payload.redirect_uri,
    }

    response = requests.post(token_url, headers=headers, data=urlencode(data))
    response.raise_for_status()
    token_data = response.json()

    return TokenExchangeResponse(
        access_token=token_data["access_token"],
        id_token=token_data.get("id_token"),
        refresh_token=token_data.get("refresh_token"),
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
    )
