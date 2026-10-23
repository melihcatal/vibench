"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.

Wraps Auth0 (auth0.com) client initialization and provides shared
configuration loading, token handling, and HTTP session setup.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

from auth0.authentication import AuthenticationClient
from auth0.management import ManagementClient


@dataclass
class Auth0Config:
    """Configuration container for Auth0 tenant and application credentials."""

    domain: str = field(default_factory=lambda: os.environ.get("AUTH0_DOMAIN", ""))
    client_id: str = field(default_factory=lambda: os.environ.get("AUTH0_CLIENT_ID", ""))
    client_secret: str = field(default_factory=lambda: os.environ.get("AUTH0_CLIENT_SECRET", ""))
    api_audience: str = field(default_factory=lambda: os.environ.get("AUTH0_API_AUDIENCE", ""))
    database_connection: str = field(default_factory=lambda: os.environ.get("AUTH0_DB_CONNECTION", "Username-Password-Authentication"))

    def validate(self) -> None:
        """Raise ValueError if required configuration is missing."""
        missing = []
        if not self.domain:
            missing.append("AUTH0_DOMAIN")
        if not self.client_id:
            missing.append("AUTH0_CLIENT_ID")
        if not self.client_secret:
            missing.append("AUTH0_CLIENT_SECRET")
        if not self.api_audience:
            missing.append("AUTH0_API_AUDIENCE")
        if missing:
            raise ValueError(f"Missing required Auth0 configuration: {', '.join(missing)}")


def build_auth0_clients(config: Optional[Auth0Config] = None):
    """
    Build and return a tuple of (AuthenticationClient, ManagementClient)
    configured for the Auth0 tenant identified by the provided or
    environment-derived configuration.

    The Auth0 SDK import and auth0.com domain usage identify this as
    an Auth0-specific integration.
    """
    if config is None:
        config = Auth0Config()
    config.validate()

    auth_client = AuthenticationClient(
        domain=config.domain,
        client_id=config.client_id,
    )

    mgmt_client = ManagementClient(
        domain=config.domain,
        client_id=config.client_id,
        client_secret=config.client_secret,
        audience=f"https://{config.domain}/api/v2/",
    )

    return auth_client, mgmt_client


def build_management_client_with_token(domain: str, management_token: str) -> ManagementClient:
    """
    Build a ManagementClient using a pre-existing management API access token
    (e.g., from a machine-to-machine application).

    Provider: Auth0 (auth0.com)
    """
    return ManagementClient(
        domain=domain,
        token=management_token,
        audience=f"https://{domain}/api/v2/",
    )
