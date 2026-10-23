import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class SecretProvider(Enum):
    AWS_SECRETS_MANAGER = "aws_secrets_manager"
    GOOGLE_SECRET_MANAGER = "google_secret_manager"
    AZURE_KEY_VAULT = "azure_key_vault"


@dataclass
class SecretConfig:
    """Configuration for secret retrieval."""

    provider: SecretProvider
    secret_name: str
    region: Optional[str] = None
    project_id: Optional[str] = None
    vault_url: Optional[str] = None
    version: Optional[str] = None


class SecurityClient:
    """Client helper utilities for Secret Management."""

    def __init__(self, config_file: str = None):
        """
        Initialize security client with configuration.

        Args:
            config_file: Path to configuration file (optional)
        """
        self.config = self._load_config(config_file)

    def _load_config(self, config_file: str = None) -> Dict[str, Any]:
        """Load configuration from file or environment."""
        config = {}

        # Try to load from file
        if config_file and os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {config_file}: {e}")

        # Override with environment variables
        env_config = {
            "aws_region": os.environ.get("AWS_REGION"),
            "gcp_project": os.environ.get("GOOGLE_CLOUD_PROJECT"),
            "azure_vault_url": os.environ.get("AZURE_KEY_VAULT_URL"),
            "default_provider": os.environ.get(
                "SECRET_PROVIDER", "aws_secrets_manager"
            ),
        }

        config.update({k: v for k, v in env_config.items() if v})
        return config

    def get_secret_config(self, secret_name: str, provider: str = None) -> SecretConfig:
        """
        Get configuration for a specific secret.

        Args:
            secret_name: Name of the secret
            provider: Provider type (optional, defaults to config)

        Returns:
            SecretConfig object
        """
        if not provider:
            provider = self.config.get("default_provider", "aws_secrets_manager")

        try:
            provider_enum = SecretProvider(provider)
        except ValueError:
            raise ValueError(
                f"Invalid provider: {provider}. Must be one of {[p.value for p in SecretProvider]}"
            )

        config = SecretConfig(
            provider=provider_enum,
            secret_name=secret_name,
            region=self.config.get("aws_region"),
            project_id=self.config.get("gcp_project"),
            vault_url=self.config.get("azure_vault_url"),
        )

        return config

    def normalize_secret_response(
        self, secret_value: Any, provider: SecretProvider
    ) -> Dict[str, Any]:
        """
        Normalize secret response across different providers.

        Args:
            secret_value: Raw secret value from provider
            provider: Provider that returned the secret

        Returns:
            Normalized secret dictionary
        """
        normalized = {
            "value": secret_value,
            "provider": provider.value,
            "timestamp": os.path.getmtime(__file__)
            if os.path.exists(__file__)
            else None,
        }

        # Add provider-specific metadata
        if provider == SecretProvider.AWS_SECRETS_MANAGER:
            normalized["provider_name"] = "AWS Secrets Manager"
        elif provider == SecretProvider.GOOGLE_SECRET_MANAGER:
            normalized["provider_name"] = "Google Cloud Secret Manager"
        elif provider == SecretProvider.AZURE_KEY_VAULT:
            normalized["provider_name"] = "Azure Key Vault"

        return normalized

    def validate_secret_name(self, secret_name: str) -> bool:
        """
        Validate secret name format.

        Args:
            secret_name: Name to validate

        Returns:
            True if valid, False otherwise
        """
        if not secret_name or not isinstance(secret_name, str):
            return False

        # Basic validation - can be extended based on provider requirements
        if len(secret_name) > 256:
            return False

        # Check for invalid characters (basic check)
        invalid_chars = [
            "<",
            ">",
            "|",
            "&",
            ";",
            "`",
            "$",
            "(",
            ")",
            "[",
            "]",
            "{",
            "}",
        ]
        for char in invalid_chars:
            if char in secret_name:
                return False

        return True
