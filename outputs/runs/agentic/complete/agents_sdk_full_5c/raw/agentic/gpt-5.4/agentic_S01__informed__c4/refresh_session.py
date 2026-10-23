from __future__ import annotations

from identity_client import FirebaseIdentityClient
from identity_models import AuthTokens, RefreshSessionRequest


def refresh_session(refresh_token: str) -> AuthTokens:
    client = FirebaseIdentityClient()
    request_model = RefreshSessionRequest(refresh_token=refresh_token)
    payload = client.post_secure_token(request_model.to_identity_payload())
    return AuthTokens(
        access_token=payload.get("id_token", ""),
        refresh_token=payload.get("refresh_token", ""),
        expires_in=int(payload.get("expires_in", 0)),
        id_token=payload.get("id_token"),
        token_type=payload.get("token_type", "Bearer"),
    )
