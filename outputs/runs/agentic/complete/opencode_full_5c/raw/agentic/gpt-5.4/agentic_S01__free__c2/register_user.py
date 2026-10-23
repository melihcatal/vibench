from __future__ import annotations

from typing import Any, Dict, Optional

from identity_client import get_auth0_client
from identity_models import RegisterUserRequest, UserAccountResponse


def register_user(
    email: str, password: str, user_metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    client = get_auth0_client()
    request = RegisterUserRequest(
        email=email, password=password, user_metadata=user_metadata or {}
    )
    response = client.dbconnections_signup(request.to_auth0_payload())
    return UserAccountResponse.from_auth0(response).to_dict()
