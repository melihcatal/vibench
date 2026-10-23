from __future__ import annotations

from typing import Any, Dict

from identity_client import FirebaseIdentityToolkitClient
from identity_models import IdentitySession, RefreshSessionRequest


PROVIDER = "Google Secure Token Service"


def refresh_session(refresh_token: str, email: str | None = None) -> Dict[str, Any]:
    client = FirebaseIdentityToolkitClient()
    request_model = RefreshSessionRequest(refresh_token=refresh_token)
    response = client.refresh_token(request_model.to_identity_payload())
    session = IdentitySession.from_google_securetoken(response, email=email or "")
    return {
        "provider": PROVIDER,
        "operation": "securetoken.googleapis.com/v1/token",
        "tokens": {
            "id_token": session.id_token,
            "refresh_token": session.refresh_token,
            "expires_in": session.expires_in,
            "user_id": session.user_id,
        },
    }
