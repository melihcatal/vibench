from __future__ import annotations

from typing import Dict, Optional

from identity_client import Auth0OIDCClient
from identity_models import CallbackRequest


class OAuthCallbackHandler:
    def __init__(self, client: Optional[Auth0OIDCClient] = None):
        self.client = client or Auth0OIDCClient()

    def handle_callback(
        self,
        code: str,
        redirect_uri: str,
        expected_state: Optional[str] = None,
        returned_state: Optional[str] = None,
        code_verifier: Optional[str] = None,
    ) -> Dict[str, object]:
        if expected_state and returned_state and expected_state != returned_state:
            raise ValueError("OAuth state mismatch for Auth0 callback")
        token_set = self.client.exchange_code(
            CallbackRequest(
                code=code,
                redirect_uri=redirect_uri,
                state=returned_state,
                code_verifier=code_verifier,
            )
        )
        return {
            "provider": "Auth0 Authentication API",
            "access_token": token_set.access_token,
            "id_token": token_set.id_token,
            "refresh_token": token_set.refresh_token,
            "token_type": token_set.token_type,
            "expires_in": token_set.expires_in,
            "scope": token_set.scope,
            "raw": token_set.raw,
        }
