"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.

Provider context: Auth0 Management API / Authentication API
- AUTH0_DOMAIN: Auth0 tenant domain (e.g., mytenant.auth0.com)
- AUTH0_CLIENT_ID: Auth0 Application Client ID
- AUTH0_CLIENT_SECRET: Auth0 Application Client Secret
"""

import os
from typing import Any, Dict, Optional

import requests


def load_auth0_config() -> Dict[str, str]:
    """Load Auth0 configuration from environment variables.

    Required env vars:
        AUTH0_DOMAIN - Auth0 tenant domain
        AUTH0_CLIENT_ID - Application client ID
        AUTH0_CLIENT_SECRET - Application client secret
    """
    domain = os.environ.get("AUTH0_DOMAIN", "").strip()
    client_id = os.environ.get("AUTH0_CLIENT_ID", "").strip()
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "").strip()

    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable is required")
    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable is required")
    if not client_secret:
        raise ValueError("AUTH0_CLIENT_SECRET environment variable is required")

    return {
        "domain": domain.rstrip("/"),
        "client_id": client_id,
        "client_secret": client_secret,
        "base_url": f"https://{domain.rstrip('/')}",
    }


def get_management_api_token(config: Dict[str, str]) -> str:
    """Obtain a Management API access token using client credentials grant.

    Uses Auth0's /oauth/token endpoint with client_credentials grant type.
    """
    token_url = f"https://{config['domain']}/oauth/token"
    payload = {
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "audience": f"https://{config['domain']}/api/v2/",
        "grant_type": "client_credentials",
    }
    response = requests.post(token_url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]


def build_auth_headers(access_token: Optional[str] = None, content_type: str = "application/json") -> Dict[str, str]:
    """Build standard HTTP headers for Auth0 API requests."""
    headers = {"Content-Type": content_type}
    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"
    return headers


def make_auth0_request(
    method: str,
    url: str,
    payload: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """Execute an HTTP request to an Auth0 endpoint with standardized error handling."""
    effective_headers = headers or build_auth_headers()
    response = requests.request(
        method=method,
        url=url,
        json=payload if method in ("POST", "PUT", "PATCH") else None,
        params=payload if method == "GET" else None,
        headers=effective_headers,
        timeout=timeout,
    )
    if not response.ok:
        try:
            error_data = response.json()
        except Exception:
            error_data = {"error": response.reason, "status_code": response.status_code}
        error_data["status_code"] = response.status_code
        raise Auth0ApiError(
            message=error_data.get("error_description", error_data.get("error", "API error")),
            status_code=response.status_code,
            error_data=error_data,
        )
    if response.content:
        return response.json()
    return {}


class Auth0ApiError(Exception):
    """Custom exception for Auth0 API errors."""

    def __init__(self, message: str, status_code: int = 0, error_data: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_data = error_data or {}


class Auth0Client:
    """Helper client that wraps common Auth0 API interactions."""

    def __init__(self, config: Optional[Dict[str, str]] = None):
        self.config = config or load_auth0_config()
        self._management_token: Optional[str] = None

    @property
    def management_token(self) -> str:
        if not self._management_token:
            self._management_token = get_management_api_token(self.config)
        return self._management_token

    def reset_token(self) -> None:
        self._management_token = None

    def post_auth(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Post to Auth0 /oauth/token for authentication flows."""
        url = f"https://{self.config['domain']}/oauth/token"
        return make_auth0_request("POST", url, payload=payload)

    def post_dbconnections_change_password(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Post to Auth0 /dbconnections/change_password."""
        url = f"https://{self.config['domain']}/dbconnections/change_password"
        payload["client_id"] = self.config["client_id"]
        return make_auth0_request("POST", url, payload=payload, content_type="application/json")

    def create_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Create a user via Auth0 Management API /api/v2/users."""
        url = f"https://{self.config['domain']}/api/v2/users"
        headers = build_auth_headers(self.management_token)
        return make_auth0_request("POST", url, payload=payload, headers=headers)
