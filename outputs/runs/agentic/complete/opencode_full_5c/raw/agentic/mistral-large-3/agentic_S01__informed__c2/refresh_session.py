import os
from identity_client import FirebaseIdentityClient
from identity_models import TokenRefreshRequest, AuthResponse, normalize_auth_response


def refresh_session(refresh_token: str) -> AuthResponse:
    client = FirebaseIdentityClient()
    response = client.refresh_token(refresh_token)
    return normalize_auth_response(
        {
            "idToken": response.get("id_token"),
            "refreshToken": response.get("refresh_token"),
            "expiresIn": response.get("expires_in"),
            "kind": response.get("token_type"),
        }
    )
