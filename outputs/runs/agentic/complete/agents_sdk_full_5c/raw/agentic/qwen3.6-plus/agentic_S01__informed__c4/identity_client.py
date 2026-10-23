"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.

Provides configuration loading, Auth0 API client setup,
and HTTP session management for identity operations.
"""

import os
from typing import Optional
import requests


class Auth0Config:
    """Configuration loader for Auth0 identity provider."""

    def __init__(self):
        self.domain: str = os.getenv("AUTH0_DOMAIN", "")
        self.client_id: str = os.getenv("AUTH0_CLIENT_ID", "")
        self.client_secret: str = os.getenv("AUTH0_CLIENT_SECRET", "")
        self.management_api_token: str = os.getenv("AUTH0_MANAGEMENT_API_TOKEN", "")
        self.api_audience: str = os.getenv("AUTH0_API_AUDIENCE", "")
        self.connection_name: str = os.getenv("AUTH0_CONNECTION", "Username-Password-Authentication")

    @property
    def issuer_url(self) -> str:
        return f"https://{self.domain}"

    @property
    def authorize_url(self) -> str:
        return f"https://{self.domain}/authorize"

    @property
    def token_url(self) -> str:
        return f"https://{self.domain}/oauth/token"

    @property
    def userinfo_url(self) -> str:
        return f"https://{self.domain}/userinfo"

    @property
    def management_api_url(self) -> str:
        return f"https://{self.domain}/api/v2"

    @property
    def is_configured(self) -> bool:
        return bool(self.domain and self.client_id)


def get_identity_config() -> Auth0Config:
    """Load and return the Auth0 configuration."""
    config = Auth0Config()
    return config


def create_management_session(config: Auth0Config) -> requests.Session:
    """Create a pre-configured requests session for Auth0 Management API calls."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {config.management_api_token}",
        "Content-Type": "application/json",
    })
    session.base_url = config.management_api_url
    return session


def create_oauth_session(config: Auth0Config) -> requests.Session:
    """Create a requests session for Auth0 OAuth2 endpoints."""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
    })
    return session
