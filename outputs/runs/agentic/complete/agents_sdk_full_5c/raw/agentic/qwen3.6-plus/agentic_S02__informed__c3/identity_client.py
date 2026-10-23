"""Provide local configuration and client helper utilities for Federated Login Flow."""

import os
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin

from identity_models import (
    AuthRequest,
    TokenExchangeRequest,
    TokenResponse,
    UserProfileClaims,
    generate_pkce_pair,
    generate_state,
)


class GoogleOIDCConfig:
    """Configuration and client helper for Google Identity Platform OIDC."""

    AUTHORIZATION_ENDPOINT = "https://accounts.google.com/o/oauth2/v2/auth"
    TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    USERINFO_ENDPOINT = "https://openidconnect.googleapis.com/v1/userinfo"
    JWKS_ENDPOINT = "https://www.googleapis.com/oauth2/v3/certs"
    ISSUER = "https://accounts.google.com"
    PROVIDER_NAME = "Google Identity Platform"

    @classmethod
    def client_id(cls) -> str:
        return os.environ.get("GOOGLE_CLIENT_ID", "")

    @classmethod
    def client_secret(cls) -> str:
        return os.environ.get("GOOGLE_CLIENT_SECRET", "")

    @classmethod
    def redirect_uri(cls) -> str:
        return os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")

    @classmethod
    def default_scopes(cls) -> List[str]:
        return ["openid", "email", "profile"]

    @classmethod
    def scopes_str(cls) -> str:
        return " ".join(cls.default_scopes())


class IdentityClient:
    """Helper client for Google Identity Platform OIDC operations."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scopes: Optional[str] = None,
    ):
        self.client_id = client_id or GoogleOIDCConfig.client_id()
        self.client_secret = client_secret or GoogleOIDCConfig.client_secret()
        self.redirect_uri = redirect_uri or GoogleOIDCConfig.redirect_uri()
        self.scopes = scopes or GoogleOIDCConfig.scopes_str()

    def create_auth_request(self, prompt: Optional[str] = None) -> AuthRequest:
        """Create an OAuth authorization request with Google OIDC defaults."""
        return AuthRequest(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            state=generate_state(),
            nonce=generate_state(),
            prompt=prompt,
        )

    def create_pkce_auth_request(self, prompt: Optional[str] = None) -> tuple:
        """Create a PKCE authorization request. Returns (AuthRequest, pkce_data)."""
        pkce_data = generate_pkce_pair()
        auth_request = AuthRequest(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scopes,
            state=generate_state(),
            nonce=generate_state(),
            code_challenge=pkce_data["code_challenge"],
            code_challenge_method="S256",
            prompt=prompt,
        )
        return auth_request, pkce_data

    def create_token_exchange_request(
        self,
        code: str,
        code_verifier: Optional[str] = None,
    ) -> TokenExchangeRequest:
        """Build a token exchange request for Google."""
        return TokenExchangeRequest(
            code=code,
            redirect_uri=self.redirect_uri,
            client_id=self.client_id,
            client_secret=self.client_secret,
            code_verifier=code_verifier,
        )

    def build_authorization_url(self, auth_request: AuthRequest) -> str:
        """Build the Google authorization URL from an AuthRequest."""
        return auth_request.to_authorization_url(GoogleOIDCConfig.AUTHORIZATION_ENDPOINT)

    def normalize_profile(self, claims: dict) -> UserProfileClaims:
        """Normalize Google OIDC claims into a UserProfileClaims object."""
        return UserProfileClaims.from_oidc_claims(claims, provider="Google Identity Platform")
