import os

from identity_client import build_client
from identity_models import RefreshRequest, as_payload


def refresh_session(refresh_token: str):
    client = build_client()
    payload = as_payload(RefreshRequest(refresh_token=refresh_token))
    payload["grant_type"] = os.environ.get("AUTH0_REFRESH_GRANT", "refresh_token")
    payload["client_id"] = os.environ.get("AUTH0_CLIENT_ID", "")
    return client.post("/oauth/token", payload)
