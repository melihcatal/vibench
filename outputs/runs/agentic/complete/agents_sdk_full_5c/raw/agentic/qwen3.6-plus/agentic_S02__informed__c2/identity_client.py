"""
identity_client.py - Local configuration and client helper utilities
for Federated Login Flow.

Provides configuration loading, OAuth state management, and token handling
utilities used across the federated login flow.
"""

import json
import os
import time
from typing import Any, Optional


class FederatedLoginConfig:
    """
    Central configuration holder for federated identity providers.
    """

    def __init__(self):
        self.auth0_domain = os.environ.get("AUTH0_DOMAIN", "")
        self.auth0_client_id = os.environ.get("AUTH0_CLIENT_ID", "")
        self.auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "")

        self.azure_tenant_id = os.environ.get("AZURE_TENANT_ID", "common")
        self.azure_client_id = os.environ.get("AZURE_CLIENT_ID", "")

        self.cognito_domain = os.environ.get("COGNITO_DOMAIN", "")
        self.cognito_client_id = os.environ.get("COGNITO_CLIENT_ID", "")

        self.default_redirect_uri = os.environ.get(
            "OAUTH_REDIRECT_URI", "http://localhost:8080/callback"
        )
        self.default_scope = os.environ.get(
            "OAUTH_DEFAULT_SCOPE", "openid profile email"
        )


class OAuthSessionStore:
    """
    In-memory store for OAuth session state and PKCE parameters.
    In production, replace with Redis or a database-backed store.
    """

    def __init__(self):
        self._sessions: dict[str, dict[str, Any]] = {}

    def store_session(self, state: str, session_data: dict) -> None:
        """Store OAuth session parameters keyed by state."""
        self._sessions[state] = {
            **session_data,
            "created_at": time.time(),
        }

    def get_session(self, state: str) -> Optional[dict]:
        """Retrieve OAuth session parameters by state."""
        return self._sessions.get(state)

    def remove_session(self, state: str) -> Optional[dict]:
        """Retrieve and remove session (one-time use)."""
        return self._sessions.pop(state, None)

    def cleanup_expired(self, max_age_seconds: int = 600) -> int:
        """Remove expired sessions. Returns count of removed sessions."""
        now = time.time()
        expired = [
            s
            for s, data in self._sessions.items()
            if now - data.get("created_at", 0) > max_age_seconds
        ]
        for s in expired:
            del self._sessions[s]
        return len(expired)


class TokenHandler:
    """
    Utility for handling OAuth/OIDC tokens.
    """

    @staticmethod
    def is_expired(expires_in: int, issued_at: float, buffer_seconds: int = 60) -> bool:
        """Check if a token is expired or about to expire."""
        return time.time() >= issued_at + expires_in - buffer_seconds

    @staticmethod
    def extract_token_type(token: str) -> str:
        """Determine token type from payload structure."""
        parts = token.split(".")
        if len(parts) == 3:
            return "jwt"
        return "opaque"

    @staticmethod
    def format_authorization_header(access_token: str, token_type: str = "Bearer") -> str:
        """Format an Authorization header value."""
        return f"{token_type} {access_token}"


# Global instances for convenience
config = FederatedLoginConfig()
session_store = OAuthSessionStore()
token_handler = TokenHandler()
