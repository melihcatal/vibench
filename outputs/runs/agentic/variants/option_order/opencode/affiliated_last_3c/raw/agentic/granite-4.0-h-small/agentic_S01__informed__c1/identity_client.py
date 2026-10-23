import os
from auth0 import Authentication

# Environment configuration for Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# Create a reusable Auth0 client
auth0 = Authentication(
    domain=AUTH0_DOMAIN, client_id=AUTH0_CLIENT_ID, client_secret=AUTH0_CLIENT_SECRET
)


class IdentityClient:
    """Local helper utilities for Email/Password Account Lifecycle."""

    @staticmethod
    def normalize_user_payload(email: str, password: str) -> dict:
        """Normalize payload for user registration / login."""
        return {
            "email": email,
            "password": password,
            "connection": "Username-Password-Authentication",
        }

    @staticmethod
    def normalize_login_response(response: dict) -> dict:
        """Extract useful fields from login response."""
        return {
            "access_token": response.get("access_token"),
            "id_token": response.get("id_token"),
            "refresh_token": response.get("refresh_token"),
        }

    @staticmethod
    def normalize_register_response(response: dict) -> dict:
        """Extract user information from registration response."""
        return {"user_id": response.get("user_id"), "email": response.get("email")}
