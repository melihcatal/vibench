from __future__ import annotations

from typing import Any, Dict

from identity_client import get_auth0_client
from identity_models import RegisterUserRequest, UserRecord


def register_user(request: RegisterUserRequest) -> Dict[str, Any]:
    client = get_auth0_client()
    payload = request.to_auth0_payload(connection=client.connection)
    user = client.management_post("/api/v2/users", payload)
    return UserRecord.from_auth0(user).to_dict()
