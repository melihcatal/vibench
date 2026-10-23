import os
import requests
from typing import Dict, Optional
from identity_client import IdentityClient
from identity_models import OAuthCallbackRequest, OAuthCallbackResponse


def handle_oauth_callback(request: OAuthCallbackRequest) -> OAuthCallbackResponse:
    client = IdentityClient()

    stored_state = client.get_state(request.state)
    if not stored_state:
        raise ValueError("Invalid or expired state")

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": request.code,
        "client_id": client.client_id,
        "client_secret": client.client_secret,
        "redirect_uri": stored_state["redirect_uri"],
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=token_data)
    response.raise_for_status()
    token_response = response.json()

    id_token = token_response.get("id_token")
    if id_token and stored_state.get("nonce"):
        client.validate_id_token(id_token, stored_state["nonce"])

    return OAuthCallbackResponse(
        access_token=token_response["access_token"],
        refresh_token=token_response.get("refresh_token"),
        id_token=id_token,
        expires_in=token_response["expires_in"],
        token_type=token_response["token_type"],
        scope=token_response.get("scope", ""),
        provider="google",
    )
