from __future__ import annotations

from typing import Dict, Optional

from identity_client import Auth0OIDCClient, generate_code_challenge, generate_code_verifier, generate_state
from identity_models import OAuthStartRequest


class PKCELoginFlow:
    def __init__(self, client: Optional[Auth0OIDCClient] = None):
        self.client = client or Auth0OIDCClient()

    def start_pkce_login(
        self,
        redirect_uri: str,
        scope: Optional[list[str]] = None,
        audience: Optional[str] = None,
    ) -> Dict[str, str]:
        state = generate_state()
        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)
        request = OAuthStartRequest(
            redirect_uri=redirect_uri,
            scope=scope or ["openid", "profile", "email"],
            state=state,
            audience=audience,
        )
        authorization_url = self.client.build_authorize_url(
            request,
            code_challenge=code_challenge,
            code_challenge_method="S256",
        )
        return {
            "provider": "Auth0 Authentication API",
            "authorization_url": authorization_url,
            "state": state,
            "code_verifier": code_verifier,
            "code_challenge_method": "S256",
        }
