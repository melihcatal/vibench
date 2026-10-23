from typing import Dict, Optional
import os
import json
from dataclasses import dataclass

# Google OAuth2 configuration
PROVIDER_CONFIGS = {
    "google": {
        "client_id": os.getenv("GOOGLE_OAUTH_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_OAUTH_CLIENT_SECRET"),
        "redirect_uri": os.getenv(
            "GOOGLE_OAUTH_REDIRECT_URI", "http://localhost:8000/auth/callback"
        ),
        "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "userinfo_url": "https://www.googleapis.com/oauth2/v3/userinfo",
        "scopes": ["openid", "email", "profile"],
    }
}


def get_oauth_config(provider: str) -> Dict:
    """Get OAuth configuration for a specific provider."""
    config = PROVIDER_CONFIGS.get(provider)
    if not config:
        raise ValueError(f"Unsupported provider: {provider}")
    return config


def get_redirect_uri() -> str:
    """Get the default redirect URI."""
    return PROVIDER_CONFIGS["google"]["redirect_uri"]
