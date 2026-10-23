from __future__ import annotations

from typing import Any, Dict

from identity_client import get_client
from identity_models import RefreshRequest


def refresh_session(request: RefreshRequest | Dict[str, Any]) -> Dict[str, Any]:
    if isinstance(request, dict):
        request = RefreshRequest(**request)
    client = get_client()
    return client.token(
        "refresh_token",
        refresh_token=request.refresh_token,
        audience=client.config.management_audience,
    )
