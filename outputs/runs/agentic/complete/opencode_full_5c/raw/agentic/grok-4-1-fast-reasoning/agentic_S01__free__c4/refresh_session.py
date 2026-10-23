from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import RefreshRequest


def refresh_session(refresh_token: str) -> Dict[str, Any]:
    req = RefreshRequest(refresh_token=refresh_token)
    client = get_identity_client()
    result = client.auth.refresh_session({"refresh_token": refresh_token})
    return dict(result)
