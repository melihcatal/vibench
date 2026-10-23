import os
from typing import Optional
import requests


class Auth0Client:
    """Client helper for Auth0 identity management."""

    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.audience = f"https://{self.domain}/api/v2/"

    def get_management_token(self) -> str:
        """Get management API token for Auth0."""
        token_url = f"https://{self.domain}/oauth/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": self.audience,
            "grant_type": "client_credentials",
        }

        response = requests.post(token_url, json=payload)
        response.raise_for_status()
        return response.json()["access_token"]

    def get_user(self, user_id: str) -> Optional[dict]:
        """Get user details from Auth0."""
        token = self.get_management_token()
        url = f"https://{self.domain}/api/v2/users/{user_id}"
        headers = {"Authorization": f"Bearer {token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        return None

    def update_user(self, user_id: str, updates: dict) -> Optional[dict]:
        """Update user details in Auth0."""
        token = self.get_management_token()
        url = f"https://{self.domain}/api/v2/users/{user_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        response = requests.patch(url, headers=headers, json=updates)
        if response.status_code == 200:
            return response.json()
        return None


def get_auth0_client() -> Auth0Client:
    """Get configured Auth0 client instance."""
    return Auth0Client()


def load_auth0_config() -> dict:
    """Load Auth0 configuration from environment."""
    return {
        "domain": os.environ.get("AUTH0_DOMAIN"),
        "client_id": os.environ.get("AUTH0_CLIENT_ID"),
        "client_secret": os.environ.get("AUTH0_CLIENT_SECRET"),
        "connection": "Username-Password-Authentication",
    }


def validate_email(email: str) -> bool:
    """Basic email validation."""
    import re

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, "Password is valid"
