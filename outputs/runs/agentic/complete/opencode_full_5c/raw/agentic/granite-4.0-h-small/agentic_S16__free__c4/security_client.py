import os
import openai


class SecurityClient:
    """Local helper providing configured client and utility methods for secret operations."""

    def __init__(self):
        self.api_base = os.getenv("SECRET_MANAGER_ENDPOINT")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = openai.SecretManager  # concrete provider client

    def get_secret(self, name: str) -> dict:
        """Retrieve a secret value using the configured provider."""
        return self.client.get_secret(name=name)

    def get_secret_version(self, name: str, version) -> dict:
        """Retrieve a specific version or staged value."""
        return self.client.get_secret_version(name=name, version=version)
