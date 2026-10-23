from __future__ import annotations

from identity_client import IdentityClient
from identity_models import RefreshRequest


def refresh_session(refresh_token: str):
    client = IdentityClient()
    return client.refresh(RefreshRequest(refresh_token=refresh_token))
