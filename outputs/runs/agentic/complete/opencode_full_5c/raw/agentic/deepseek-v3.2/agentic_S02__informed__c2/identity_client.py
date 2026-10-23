import os
import json
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ClientConfig:
    """Configuration for identity client."""

    provider: str = "auth0"
    domain: Optional[str] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_base: Optional[str] = None

    @classmethod
    def from_env(cls):
        """Load configuration from environment variables."""
        return cls(
            provider=os.environ.get("IDENTITY_PROVIDER", "auth0"),
            domain=os.environ.get("AUTH0_DOMAIN"),
            client_id=os.environ.get("AUTH0_CLIENT_ID"),
            client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
            redirect_base=os.environ.get("REDIRECT_BASE_URL"),
        )


class IdentityClient:
    """Client helper utilities for federated login flow."""

    def __init__(self, config: Optional[ClientConfig] = None):
        self.config = config or ClientConfig.from_env()
        self._auth_states = {}
        self._pkce_states = {}
        self._tokens = {}

    def store_auth_state(self, state: str, nonce: str, redirect_uri: str):
        """Store authorization state for validation."""
        self._auth_states[state] = {
            "nonce": nonce,
            "redirect_uri": redirect_uri,
            "timestamp": time.time(),
        }

    def validate_auth_state(self, state: str, redirect_uri: str) -> bool:
        """Validate authorization state."""
        if state not in self._auth_states:
            return False

        state_data = self._auth_states[state]

        # Check redirect URI matches
        if state_data["redirect_uri"] != redirect_uri:
            return False

        # Check state hasn't expired (5 minutes)
        if time.time() - state_data["timestamp"] > 300:
            del self._auth_states[state]
            return False

        return True

    def get_auth_nonce(self, state: str) -> Optional[str]:
        """Get nonce for given state."""
        if state in self._auth_states:
            return self._auth_states[state]["nonce"]
        return None

    def store_pkce_state(
        self, state: str, nonce: str, redirect_uri: str, code_verifier: str
    ):
        """Store PKCE state for validation."""
        self._pkce_states[state] = {
            "nonce": nonce,
            "redirect_uri": redirect_uri,
            "code_verifier": code_verifier,
            "timestamp": time.time(),
        }

    def validate_pkce_state(self, state: str, redirect_uri: str) -> bool:
        """Validate PKCE state."""
        if state not in self._pkce_states:
            return False

        state_data = self._pkce_states[state]

        # Check redirect URI matches
        if state_data["redirect_uri"] != redirect_uri:
            return False

        # Check state hasn't expired (5 minutes)
        if time.time() - state_data["timestamp"] > 300:
            del self._pkce_states[state]
            return False

        return True

    def get_pkce_verifier(self, state: str) -> Optional[str]:
        """Get PKCE code verifier for given state."""
        if state in self._pkce_states:
            return self._pkce_states[state]["code_verifier"]
        return None

    def store_tokens(self, state: str, token_response: Any):
        """Store tokens for a given state."""
        self._tokens[state] = {"response": token_response, "timestamp": time.time()}

    def get_tokens(self, state: str) -> Optional[Any]:
        """Get tokens for a given state."""
        if state in self._tokens:
            return self._tokens[state]["response"]
        return None

    def clear_state(self, state: str):
        """Clear all stored data for a state."""
        self._auth_states.pop(state, None)
        self._pkce_states.pop(state, None)
        self._tokens.pop(state, None)

    def build_redirect_uri(self, path: str = "/callback") -> str:
        """Build redirect URI from base URL."""
        if not self.config.redirect_base:
            raise ValueError("Redirect base URL not configured")
        return f"{self.config.redirect_base.rstrip('/')}{path}"
