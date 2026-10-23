"""
Local configuration and client helper utilities for Email/Password Account Lifecycle.
Provides Auth0-specific client initialization, configuration loading, and HTTP helpers.
"""

import os
from typing import Optional
import requests


AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "dev-example.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "")
AUTH0_MANAGEMENT_API_TOKEN = os.getenv("AUTH0_MANAGEMENT_API_TOKEN", "")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE", f"https://{AUTH0_DOMAIN}/api/v2/")
AUTH0_DATABASE_CONNECTION = os.getenv("AUTH0_DATABASE_CONNECTION", "Username-Password-Authentication")


def get_auth0_base_url() -> str:
    """Return the base URL for Auth0 authentication endpoints."""
    return f"https://{AUTH0_DOMAIN}"


def get_auth0_management_url() -> str:
    """Return the base URL for Auth0 Management API."""
    return f"https://{AUTH0_DOMAIN}/api/v2"


def get_management_headers() -> dict:
    """Return headers required for Auth0 Management API calls."""
    return {
        "Authorization": f"Bearer {AUTH0_MANAGEMENT_API_TOKEN}",
        "Content-Type": "application/json",
    }


def get_authentication_client() -> requests.Session:
    """Create a requests session pre-configured for Auth0 Authentication API."""
    session = requests.Session()
    session.base_url = get_auth0_base_url()
    return session


def get_management_client() -> requests.Session:
    """Create a requests session pre-configured for Auth0 Management API."""
    session = requests.Session()
    session.headers.update(get_management_headers())
    session.base_url = get_auth0_management_url()
    return session


def build_auth0_token_url() -> str:
    """Build the OAuth2 token endpoint URL for Auth0."""
    return f"{get_auth0_base_url()}/oauth/token"


def build_auth0_db_connection_endpoint(action: str) -> str:
    """Build the DB Connections endpoint URL for a given action."""
    return f"{get_auth0_base_url()}/dbconnections/{action}"


def build_auth0_change_password_url() -> str:
    """Build the change password endpoint URL."""
    return f"{get_auth0_base_url()}/dbconnections/change_password"


def build_auth0_signup_url() -> str:
    """Build the signup endpoint URL."""
    return f"{get_auth0_base_url()}/dbconnections/signup"


def build_auth0_reset_password_url() -> str:
    """Build the reset password endpoint URL."""
    return f"{get_auth0_base_url()}/dbconnections/change_password"
