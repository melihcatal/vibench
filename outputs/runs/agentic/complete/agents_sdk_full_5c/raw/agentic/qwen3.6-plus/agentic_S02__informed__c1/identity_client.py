"""
Local configuration and client helper utilities for Federated Login Flow.

Provides Auth0-specific configuration loading, state management helpers,
and client utilities used by the OAuth/OIDC integration files.
"""

import json
import os
from typing import Any, Dict, List, Optional

from identity_models import OAuthState, TokenResponse, UserProfile, AuditEvent


class Auth0Config:
    """Configuration helper for Auth0 Authentication API (auth0.com)."""

    def __init__(
        self,
        domain: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        connection: Optional[str] = None,
        audience: Optional[str] = None,
    ):
        self.domain = domain or os.environ.get("AUTH0_DOMAIN", "")
        self.client_id = client_id or os.environ.get("AUTH0_CLIENT_ID", "")
        self.client_secret = client_secret or os.environ.get("AUTH0_CLIENT_SECRET", "")
        self.redirect_uri = redirect_uri or os.environ.get("AUTH0_REDIRECT_URI", "")
        self.connection = connection or os.environ.get("AUTH0_CONNECTION", "")
        self.audience = audience or os.environ.get("AUTH0_AUDIENCE", "")

        if not self.domain:
            raise ValueError("AUTH0_DOMAIN environment variable is required")
        if not self.client_id:
            raise ValueError("AUTH0_CLIENT_ID environment variable is required")

    @property
    def issuer(self) -> str:
        return f"https://{self.domain}"

    @property
    def authorization_endpoint(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_endpoint(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_endpoint(self) -> str:
        return f"https://{self.domain}/userinfo"

    @property
    def jwks_uri(self) -> str:
        return f"https://{self.domain}/.well-known/jwks.json"

    @property
    def oidc_discovery_url(self) -> str:
        return f"https://{self.domain}/.well-known/openid-configuration"

    def build_scopes(self, extra_scopes: Optional[List[str]] = None) -> str:
        base = ["openid", "profile", "email"]
        if extra_scopes:
            base.extend(extra_scopes)
        return " ".join(base)


class StateStore:
    """In-memory OAuth state store for tracking authorization requests."""

    def __init__(self):
        self._states: Dict[str, OAuthState] = {}

    def store(self, state: OAuthState) -> None:
        self._states[state.state] = state

    def retrieve(self, state_value: str) -> Optional[OAuthState]:
        return self._states.pop(state_value, None)

    def exists(self, state_value: str) -> bool:
        return state_value in self._states


class TokenStore:
    """In-memory token cache keyed by user sub."""

    def __init__(self):
        self._tokens: Dict[str, TokenResponse] = {}

    def store(self, sub: str, token_response: TokenResponse) -> None:
        self._tokens[sub] = token_response

    def retrieve(self, sub: str) -> Optional[TokenResponse]:
        return self._tokens.get(sub)


class AuditLogger:
    """In-memory audit event collector."""

    def __init__(self):
        self._events: List[AuditEvent] = []

    def log(self, event: AuditEvent) -> None:
        self._events.append(event)

    def get_events(self) -> List[AuditEvent]:
        return list(self._events)

    def get_events_for_user(self, sub: str) -> List[AuditEvent]:
        return [e for e in self._events if e.sub == sub]


# Module-level singletons for convenience
_state_store = StateStore()
_token_store = TokenStore()
_audit_logger = AuditLogger()


def get_state_store() -> StateStore:
    return _state_store


def get_token_store() -> TokenStore:
    return _token_store


def get_audit_logger() -> AuditLogger:
    return _audit_logger


def load_config() -> Auth0Config:
    return Auth0Config()
