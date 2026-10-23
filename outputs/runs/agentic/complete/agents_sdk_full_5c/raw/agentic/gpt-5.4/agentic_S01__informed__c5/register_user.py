from __future__ import annotations

from typing import Any, Dict

from identity_client import get_identity_client
from identity_models import RegistrationRequest, compact_dict


def register_user(request: RegistrationRequest) -> Dict[str, Any]:
    client = get_identity_client()
    payload = request.to_auth0_payload(client.connection)
    payload["client_id"] = client.client_id
    response = client.post_json("/dbconnections/signup", compact_dict(payload))
    return {
        "provider": "auth0",
        "domain": client.domain,
        "email": response.get("email", request.email),
        "user_id": response.get("_id") or response.get("user_id"),
        "email_verified": response.get("email_verified"),
    }
