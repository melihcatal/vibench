import os
import json
from typing import Any, Dict, Optional

# HELPER: Central client for Email/Password Account Lifecycle operations


class IdentityClient:
    """Generic identity provider client for local service integration.

    Attributes:
        provider: Identifier for the selected provider (used for logging/validation).
        config: Service-specific credentials and endpoint settings.
        api_base: Base URL for the provider's HTTP API (if applicable).
    """

    def __init__(self, provider: str, config: Dict[str, Any]):
        self.provider = provider
        self.config = config
        self.api_base = config.get("api_base", "https://api.example.com")

    def _build_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        # Optional Bearer token placeholder for providers that need auth on every call
        if self.config.get("auth_token"):
            headers["Authorization"] = f"Bearer {self.config['auth_token']}"
        return headers

    def call_api(
        self, method: str, path: str, json: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Invoke the provider's HTTP API and return parsed JSON.

        Args:
            method: HTTP verb (GET, POST, ...).
            path: Relative path (e.g., "/register").
            json: Payload dictionary.

        Returns:
            Parsed JSON response.
        """
        import requests

        url = f"{self.api_base}{path}"
        response = requests.request(
            method, url, headers=self._build_headers(), json=json, timeout=10
        )
        self._handle_errors(response)
        return response.json()

    def _handle_errors(self, response: requests.Response):
        if not (200 <= response.status_code < 300):
            try:
                error_msg = response.json().get("error", response.text)
            except Exception:
                error_msg = response.text
            raise RuntimeError(
                f"Provider {self.provider} error: {error_msg} (status {response.status_code})"
            )

    # Provider-specific payload builders (example stubs)
    def build_register_payload(self, email: str, password: str) -> Dict[str, Any]:
        return {"email": email, "password": password}

    def build_login_payload(self, email: str, password: str) -> Dict[str, Any]:
        return {"email": email, "password": password}

    def build_refresh_payload(self, refresh_token: str) -> Dict[str, Any]:
        return {"refresh_token": refresh_token}

    def build_reset_payload(self, email: str) -> Dict[str, Any]:
        return {"email": email}

    def validate_response(self, response: Dict[str, Any], operation: str):
        # Simple schema validation placeholder - adjust per provider expectations
        if not isinstance(response, dict) or "error" in response:
            raise RuntimeError(
                f"Invalid {operation} response from {self.provider}: {response}"
            )
