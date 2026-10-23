
import json
import os
from typing import Dict, Any

class IdentityClient:
    """
    Provides local configuration and client helper utilities for Federated Login Flow.
    """

    def __init__(self, config_path: str = "identity_config.json"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Loads configuration from a JSON file."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}

    def get_provider_config(self, provider_name: str) -> Dict[str, Any]:
        """
        Retrieves configuration for a specific identity provider.

        Args:
            provider_name: The name of the identity provider (e.g., "google", "azure").

        Returns:
            A dictionary containing the provider's configuration, or an empty dictionary
            if the provider is not found.
        """
        return self._config.get("providers", {}).get(provider_name, {})

    def get_client_id(self, provider_name: str) -> str | None:
        """
        Retrieves the client ID for a specific identity provider.

        Args:
            provider_name: The name of the identity provider.

        Returns:
            The client ID string, or None if not found.
        """
        provider_config = self.get_provider_config(provider_name)
        return provider_config.get("client_id")

    def get_redirect_uri(self, provider_name: str) -> str | None:
        """
        Retrieves the redirect URI for a specific identity provider.

        Args:
            provider_name: The name of the identity provider.

        Returns:
            The redirect URI string, or None if not found.
        """
        provider_config = self.get_provider_config(provider_name)
        return provider_config.get("redirect_uri")

    def get_auth_endpoint(self, provider_name: str) -> str | None:
        """
        Retrieves the authorization endpoint for a specific identity provider.

        Args:
            provider_name: The name of the identity provider.

        Returns:
            The authorization endpoint URL string, or None if not found.
        """
        provider_config = self.get_provider_config(provider_name)
        return provider_config.get("auth_endpoint")

    def get_token_endpoint(self, provider_name: str) -> str | None:
        """
        Retrieves the token endpoint for a specific identity provider.

        Args:
            provider_name: The name of the identity provider.

        Returns:
            The token endpoint URL string, or None if not found.
        """
        provider_config = self.get_provider_config(provider_name)
        return provider_config.get("token_endpoint")

    def get_userinfo_endpoint(self, provider_name: str) -> str | None:
        """
        Retrieves the user information endpoint for a specific identity provider.

        Args:
            provider_name: The name of the identity provider.

        Returns:
            The user information endpoint URL string, or None if not found.
        """
        provider_config = self.get_provider_config(provider_name)
        return provider_config.get("userinfo_endpoint")

    # Add more helper methods as needed for specific federated login flows
    # For example, methods to construct authorization URLs, exchange codes for tokens, etc.
