import os
from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import RefreshSessionRequest, RefreshSessionResponse


def refresh_session(refresh_token: str) -> RefreshSessionResponse:
    client = get_identity_client()
    
    response = client.refresh_access_token(
        refresh_token=refresh_token
    )
    
    return RefreshSessionResponse(
        access_token=response["access_token"],
        expires_in=response["expires_in"]
    )