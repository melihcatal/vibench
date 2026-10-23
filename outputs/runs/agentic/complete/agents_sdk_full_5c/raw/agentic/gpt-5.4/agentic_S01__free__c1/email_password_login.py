from __future__ import annotations

from typing import Any, Dict

from identity_client import FirebaseIdentityToolkitClient
from identity_models import IdentitySession, LoginRequest


PROVIDER = "Google Identity Platform"


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    client = FirebaseIdentityToolkitClient()
    request_model = LoginRequest(email=email, password=password)
    response = client.sign_in_with_password(request_model.to_identity_payload())
    session = IdentitySession.from_google_identity_toolkit(response)
    return {
        "provider": PROVIDER,
        "operation": "accounts:signInWithPassword",
        "tokens": {
            "id_token": session.id_token,
            "refresh_token": session.refresh_token,
            "expires_in": session.expires_in,
        },
        "user": {
            "user_id": session.user_id,
            "email": session.email,
            "registered": response.get("registered", True),
        },
    }
