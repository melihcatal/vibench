# Federated Login Flow - Identity Client Utilities

import os
import json
import base64
import hashlib
import secrets
from typing import Dict, Optional, Tuple

from auth0.authentication import GetToken
from auth0.management import Auth0


class IdentityClient:
    """Client helper for Auth0 OIDC federation."""

    def __init__(self):
        self.domain = os.getenv("AUTH0_DOMAIN")
        self.client_id = os.getenv("AUTH0_CLIENT_ID")
        self.client_secret = os.getenv("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"
        self.token_endpoint = f"https://{self.domain}/oauth/token"
        self.authorization_endpoint = f"https://{self.domain}/authorize"
        self.jwks_uri = f"https://{self.domain}/.well-known/jwks.json"
        self.issuer = f"https://{self.domain}/"

    def generate_pkce_pair(self) -> Tuple[str, str]:
        """Generate PKCE code_verifier and code_challenge."""
        code_verifier = secrets.token_urlsafe(64)
        code_challenge = (
            base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
            .decode()
            .rstrip("=")
        )
        return code_verifier, code_challenge

    def get_oauth_token(
        self, code: str, redirect_uri: str, code_verifier: Optional[str] = None
    ) -> Dict:
        """Exchange authorization code for tokens."""
        get_token = GetToken(self.domain)
        token = get_token.authorization_code(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=redirect_uri,
            code_verifier=code_verifier,
        )
        return token

    def get_user_info(self, access_token: str) -> Dict:
        """Fetch user profile claims."""
        auth0 = Auth0(self.domain, access_token)
        return auth0.users.get("me")
