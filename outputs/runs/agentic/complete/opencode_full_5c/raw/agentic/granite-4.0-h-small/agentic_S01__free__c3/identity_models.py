# [HELPER] identity_models.py
# Define local request, response, and normalization helpers for Email/Password Account Lifecycle

from typing import Dict, Any, Optional

# User registration request/response shapes (normalized toward Auth0 API)
RegistrationRequest = Dict[str, Any]
RegistrationResponse = Dict[str, Any]

# Login request/response shapes
LoginRequest = Dict[str, Any]
LoginResponse = Dict[str, Any]

# Refresh token request/response shapes
RefreshRequest = Dict[str, Any]
RefreshResponse = Dict[str, Any]


def normalize_registration_response(raw: Dict[str, Any]) -> RegistrationResponse:
    """Strip Auth0-specific wrappers and return a clean user record."""
    # Auth0 returns the full user object directly on success
    return raw


def normalize_login_response(raw: Dict[str, Any]) -> LoginResponse:
    """Extract tokens from the standard login payload."""
    return {
        "access_token": raw.get("access_token"),
        "id_token": raw.get("id_token"),
        "refresh_token": raw.get("refresh_token"),
        "expires_in": raw.get("expires_in"),
    }


def normalize_refresh_response(raw: Dict[str, Any]) -> RefreshResponse:
    return {
        "access_token": raw.get("access_token"),
        "id_token": raw.get("id_token"),
        "refresh_token": raw.get("refresh_token"),
        "expires_in": raw.get("expires_in"),
    }


# Helper to build full URL for API calls (optional)
BASE_URL = os.getenv("BASE_URL", "https://your-auth0-domain.auth0.com")


def api_url(path: str) -> str:
    return f"{BASE_URL}{path}"
