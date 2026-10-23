from __future__ import annotations

from identity_client import CognitoIdentityClient
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    request = RefreshRequest(refresh_token=refresh_token)
    return CognitoIdentityClient().refresh(request.refresh_token)
