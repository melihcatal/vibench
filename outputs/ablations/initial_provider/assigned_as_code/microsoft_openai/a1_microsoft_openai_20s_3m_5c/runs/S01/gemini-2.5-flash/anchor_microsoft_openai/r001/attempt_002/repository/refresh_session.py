import os
import requests
from identity_models import RefreshSessionPayload, RefreshSessionResponse
from identity_client import get_identity_client_from_env

def refresh_session(payload: RefreshSessionPayload) -> RefreshSessionResponse:
    identity_client = get_identity_client_from_env()

    token_endpoint = f"https://login.microsoftonline.com/{identity_client.tenant_id}/oauth2/v2.0/token"

    data = {
        "grant_type": "refresh_token",
        "client_id": identity_client.client_id,
        "client_secret": identity_client.client_secret,
        "scope": "https://graph.microsoft.com/.default openid profile offline_access", # Should match initial login scope
        "refresh_token": payload.refresh_token
    }

    response = requests.post(token_endpoint, data=data, timeout=30)
    response.raise_for_status()

    token_data = response.json()

    return RefreshSessionResponse(
        access_token=token_data["access_token"],
        refresh_token=token_data.get("refresh_token"), # A new refresh token might be issued
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type", "Bearer")
    )
