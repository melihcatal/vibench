from __future__ import annotations

from typing import Any, Dict, Optional

from identity_client import get_auth0_client
from identity_models import RefreshSessionRequest, TokenResponse


def refresh_session(refresh_token: str, scope: Optional[str] = None) -> Dict[str, Any]:
    client = get_auth0_client()
    request = RefreshSessionRequest(refresh_token=refresh_token, scope=scope)
    response = client.oauth_token_refresh(request.refresh_token, request.scope)
    return TokenResponse.from_auth0(response).to_dict()
