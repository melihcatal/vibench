import os
from typing import Dict
from identity_client import IdentityClient
from identity_models import RefreshSessionRequest, normalize_refresh_response


def refresh_session(refresh_token: str) -> Dict[str, str]:
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")

    request = RefreshSessionRequest(
        refresh_token=refresh_token, client_id=client_id, client_secret=client_secret
    )

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token,
        "client_id": request.client_id,
        "client_secret": request.client_secret,
    }

    response = IdentityClient().post("oauth/token", payload)
    normalized_response = normalize_refresh_response(response)

    return {
        "access_token": normalized_response.access_token,
        "id_token": normalized_response.id_token,
        "expires_in": str(normalized_response.expires_in),
    }
