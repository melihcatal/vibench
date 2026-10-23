from __future__ import annotations

from typing import Any, Dict

from identity_client import FirebaseIdentityToolkitClient
from identity_models import IdentitySession, RegisterUserRequest, compact_dict


PROVIDER = "Google Identity Platform"


def register_user(email: str, password: str, display_name: str | None = None) -> Dict[str, Any]:
    client = FirebaseIdentityToolkitClient()
    request_model = RegisterUserRequest(email=email, password=password, display_name=display_name)
    payload = request_model.to_identity_payload()
    response = client.sign_up(payload)
    session = IdentitySession.from_google_identity_toolkit(response)
    return compact_dict(
        {
            "provider": PROVIDER,
            "operation": "accounts:signUp",
            "user": {
                "user_id": response.get("localId"),
                "email": response.get("email"),
                "display_name": display_name,
            },
            "session": session.to_dict(),
        }
    )
