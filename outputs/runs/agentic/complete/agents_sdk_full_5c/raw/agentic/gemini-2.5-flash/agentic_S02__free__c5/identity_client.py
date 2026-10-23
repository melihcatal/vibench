import os

class IdentityClientConfig:
    """Provides centralized configuration for identity providers."""

    # Google OAuth 2.0
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback")
    GOOGLE_SCOPES = "openid profile email"

    # Auth0 PKCE
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN", "YOUR_AUTH0_DOMAIN.auth0.com")
    AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID", "YOUR_AUTH0_CLIENT_ID")
    AUTH0_REDIRECT_URI = os.environ.get("AUTH0_REDIRECT_URI", "http://localhost:8000/auth0_callback")
    AUTH0_SCOPE = "openid profile email"

class IdentityClientUtils:
    """Utility functions for identity-related operations."""

    @staticmethod
    def build_query_string(params: dict) -> str:
        """Builds a URL query string from a dictionary of parameters."""
        import urllib.parse
        return urllib.parse.urlencode(params)

    @staticmethod
    def generate_random_string(length: int = 32) -> str:
        """Generates a cryptographically secure random string."""
        import secrets
        return secrets.token_urlsafe(length)

# Example of how you might use these in other files:
# from identity_client import IdentityClientConfig, IdentityClientUtils
# client_id = IdentityClientConfig.GOOGLE_CLIENT_ID
# random_str = IdentityClientUtils.generate_random_string()
