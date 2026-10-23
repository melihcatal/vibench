import os

class IdentityClient:
    """Local helper that stores Auth0 credentials and provides helpers for SDK/initiation."""

    def __init__(self):
        # In a real deployment these would be kept secret and read from env vars or secret manager
        self.auth0_domain = os.getenv("AUTH0_DOMAIN", "dev-1234567.auth0.com")  # <-- Auth0 tenant domain
        self.auth0_client_id = os.getenv("AUTH0_CLIENT_ID", "YOUR_CLIENT_ID")
        self.auth0_client_secret = os.getenv("AUTH0_CLIENT_SECRET", "YOUR_CLIENT_SECRET")
        self.auth0_management_token = os.getenv("AUTH0_MANAGEMENT_TOKEN", "MGMT_TOKEN_PLACEHOLDER")
        self.auth0_api_audience = os.getenv("AUTH0_API_AUDIENCE", "https://YOUR_TENANT.auth0.com/api/v2/")

    def get_management_headers(self):
        """Return headers needed for Auth0 Management API calls."""
        return {
            "Authorization": f"Bearer {self.auth0_management_token}",
            "Content-Type": "application/json",
        }
