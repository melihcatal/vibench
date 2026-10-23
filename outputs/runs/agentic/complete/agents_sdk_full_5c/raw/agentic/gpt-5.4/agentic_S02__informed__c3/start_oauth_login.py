from __future__ import annotations

from typing import Dict, Optional

from identity_client import Auth0OIDCClient, generate_state
from identity_models import OAuthStartRequest


class OAuthLoginStarter:
    def __init__(self, client: Optional[Auth0OIDCClient] = None):
        self.client = client or Auth0OIDCClient()

    def start_login(
        self,
        redirect_uri: str,
        scope: Optional[list[str]] = None,
        audience: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> Dict[str, str]:
        state = generate_state()
        request = OAuthStartRequest(
            redirect_uri=redirect_uri,
            scope=scope or ["openid", "profile", "email"],
            state=state,
            audience=audience,
            prompt=prompt,
        )
        authorization_url = self.client.build_authorize_url(request)
        return {
            "provider": "Auth0 Authentication API",
            "authorization_url": authorization_url,
            "state": state,
            "issuer": self.client.config.issuer,
        }
