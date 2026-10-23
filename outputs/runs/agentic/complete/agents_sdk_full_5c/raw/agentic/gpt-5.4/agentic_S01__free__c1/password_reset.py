from __future__ import annotations

from typing import Any, Dict

from identity_client import FirebaseIdentityToolkitClient
from identity_models import PasswordResetRequest


PROVIDER = "Google Identity Platform"


def password_reset(email: str) -> Dict[str, Any]:
    client = FirebaseIdentityToolkitClient()
    request_model = PasswordResetRequest(email=email)
    response = client.send_oob_code(request_model.to_identity_payload())
    return {
        "provider": PROVIDER,
        "operation": "accounts:sendOobCode",
        "email": response.get("email", email),
        "request_type": "PASSWORD_RESET",
    }
