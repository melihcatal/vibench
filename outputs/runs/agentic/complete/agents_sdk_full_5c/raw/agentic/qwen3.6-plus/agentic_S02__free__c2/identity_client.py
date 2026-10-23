"""
identity_client.py - Local configuration and client helper utilities for Federated Login Flow

Provides centralized configuration loading for Auth0 OIDC integration
and shared HTTP client utilities.
"""

import os
from typing import Dict, Any, Optional
from functools import lru_cache


def get_auth0_config() -> Dict[str, str]:
    """
    Load Auth0 configuration from environment variables.

    Required environment variables:
    - AUTH0_DOMAIN: e.g. "my-tenant.auth0.com"
    - AUTH0_CLIENT_ID: Auth0 application client ID
    - AUTH0_CLIENT_SECRET: Auth0 application client secret

    Optional:
    - AUTH0_AUDIENCE: Default API audience identifier
    - AUTH0_CALLBACK_URL: Default callback/redirect URI
    """
    domain = os.environ.get("AUTH0_DOMAIN", "").strip()
    client_id = os.environ.get("AUTH0_CLIENT_ID", "").strip()
    client_secret = os.environ.get("AUTH0_CLIENT_SECRET", "").strip()
    audience = os.environ.get("AUTH0_AUDIENCE", "").strip()
    callback_url = os.environ.get("AUTH0_CALLBACK_URL", "").strip()

    if not domain:
        raise ValueError("AUTH0_DOMAIN environment variable is required")
    if not client_id:
        raise ValueError("AUTH0_CLIENT_ID environment variable is required")
    if not client_secret:
        raise ValueError("AUTH0_CLIENT_SECRET environment variable is required")

    return {
        "auth0_domain": domain,
        "auth0_client_id": client_id,
        "auth0_client_secret": client_secret,
        "auth0_audience": audience,
        "auth0_callback_url": callback_url,
    }


def get_auth0_domain() -> str:
    """Return the configured Auth0 domain."""
    return get_auth0_config()["auth0_domain"]


def build_auth0_url(path: str) -> str:
    """Build a fully qualified Auth0 URL for a given path."""
    domain = get_auth0_domain()
    base = f"https://{domain}"
    clean_path = path.lstrip("/")
    return f"{base}/{clean_path}"


def validate_redirect_uri(redirect_uri: str, allowed_uris: Optional[list] = None) -> bool:
    """
    Validate that a redirect URI is in the allowed list.

    If no allowed_uris provided, checks against AUTH0_CALLBACK_URL.
    """
    if allowed_uris is None:
        config = get_auth0_config()
        allowed_uris = [config["auth0_callback_url"]] if config["auth0_callback_url"] else []

    return redirect_uri in allowed_uris


def normalize_scope(scope_input: Optional[str]) -> str:
    """
    Normalize OAuth scope string, ensuring openid is always present.

    Auth0 requires 'openid' for OIDC flows.
    """
    if not scope_input:
        return "openid profile email"

    scopes = set(scope_input.split())
    scopes.add("openid")
    return " ".join(sorted(scopes))
