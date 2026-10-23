import os
import json
from typing import Dict, Any, Optional


def load_oauth_config() -> Dict[str, Any]:
    """Load OAuth configuration from environment or config file."""
    config = {
        "google": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
            "redirect_uri": os.getenv(
                "GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/callback/google"
            ),
            "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "token_endpoint": "https://oauth2.googleapis.com/token",
            "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo",
            "scope": "openid email profile",
            "supports_pkce": True,
            "use_nonce": True,
        },
        "microsoft": {
            "client_id": os.getenv("MICROSOFT_CLIENT_ID", ""),
            "client_secret": os.getenv("MICROSOFT_CLIENT_SECRET", ""),
            "redirect_uri": os.getenv(
                "MICROSOFT_REDIRECT_URI",
                "http://localhost:8000/auth/callback/microsoft",
            ),
            "authorization_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "token_endpoint": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            "userinfo_endpoint": "https://graph.microsoft.com/oidc/userinfo",
            "scope": "openid email profile",
            "supports_pkce": True,
            "use_nonce": True,
        },
        "github": {
            "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
            "client_secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
            "redirect_uri": os.getenv(
                "GITHUB_REDIRECT_URI", "http://localhost:8000/auth/callback/github"
            ),
            "authorization_endpoint": "https://github.com/login/oauth/authorize",
            "token_endpoint": "https://github.com/login/oauth/access_token",
            "userinfo_endpoint": "https://api.github.com/user",
            "scope": "user:email",
            "supports_pkce": True,
            "use_nonce": False,
        },
        "auth0": {
            "client_id": os.getenv("AUTH0_CLIENT_ID", ""),
            "client_secret": os.getenv("AUTH0_CLIENT_SECRET", ""),
            "redirect_uri": os.getenv(
                "AUTH0_REDIRECT_URI", "http://localhost:8000/auth/callback/auth0"
            ),
            "authorization_endpoint": f"https://{os.getenv('AUTH0_DOMAIN', '')}/authorize",
            "token_endpoint": f"https://{os.getenv('AUTH0_DOMAIN', '')}/oauth/token",
            "userinfo_endpoint": f"https://{os.getenv('AUTH0_DOMAIN', '')}/userinfo",
            "scope": "openid email profile",
            "supports_pkce": True,
            "use_nonce": True,
        },
    }

    return config


def get_oauth_client_config(provider: str) -> Dict[str, Any]:
    """Get OAuth configuration for a specific provider."""
    config = load_oauth_config()

    if provider not in config:
        raise ValueError(f"Unsupported OAuth provider: {provider}")

    provider_config = config[provider]

    if not provider_config["client_id"]:
        raise ValueError(f"Missing client_id for provider: {provider}")

    return provider_config


def get_userinfo_endpoint(provider: str) -> str:
    """Get userinfo endpoint for a provider."""
    config = get_oauth_client_config(provider)
    return config["userinfo_endpoint"]


def validate_token_response(
    token_response: Dict[str, Any], provider: str
) -> Dict[str, Any]:
    """Validate token response from OAuth provider."""
    required_fields = ["access_token", "token_type"]

    for field in required_fields:
        if field not in token_response:
            raise ValueError(f"Missing required field in token response: {field}")

    if (
        provider in ["google", "microsoft", "auth0"]
        and "id_token" not in token_response
    ):
        raise ValueError(f"Missing id_token in token response for provider: {provider}")

    return token_response


def get_provider_display_name(provider: str) -> str:
    """Get display name for a provider."""
    display_names = {
        "google": "Google",
        "microsoft": "Microsoft",
        "github": "GitHub",
        "auth0": "Auth0",
    }

    return display_names.get(provider, provider.capitalize())


def is_provider_enabled(provider: str) -> bool:
    """Check if a provider is enabled (has configuration)."""
    try:
        config = get_oauth_client_config(provider)
        return bool(config["client_id"])
    except ValueError:
        return False


def get_enabled_providers() -> list:
    """Get list of enabled OAuth providers."""
    config = load_oauth_config()
    enabled = []

    for provider in config:
        if is_provider_enabled(provider):
            enabled.append(provider)

    return enabled
