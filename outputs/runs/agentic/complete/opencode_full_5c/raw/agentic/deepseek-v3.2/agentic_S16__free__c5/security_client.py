import os
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from enum import Enum


class SecretProvider(Enum):
    AWS_SECRETS_MANAGER = "aws_secrets_manager"
    GCP_SECRET_MANAGER = "gcp_secret_manager"
    AZURE_KEY_VAULT = "azure_key_vault"
    HASHICORP_VAULT = "hashicorp_vault"


@dataclass
class SecretConfig:
    """Configuration for secret management clients."""

    provider: SecretProvider
    region: Optional[str] = None
    project_id: Optional[str] = None
    vault_url: Optional[str] = None
    vault_token: Optional[str] = None
    timeout: int = 30
    retry_attempts: int = 3
    cache_ttl: int = 300  # 5 minutes


@dataclass
class SecretResponse:
    """Normalized response from secret providers."""

    name: str
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    provider: Optional[SecretProvider] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding sensitive value in metadata."""
        result = asdict(self)
        if "value" in result and result["value"]:
            result["value"] = "***REDACTED***"
        return result


class SecurityClient:
    """Client helper utilities for secret management."""

    @staticmethod
    def load_config_from_env() -> SecretConfig:
        """Load configuration from environment variables."""
        provider_str = os.environ.get("SECRET_PROVIDER", "aws_secrets_manager").lower()

        try:
            provider = SecretProvider(provider_str)
        except ValueError:
            provider = SecretProvider.AWS_SECRETS_MANAGER

        config = SecretConfig(
            provider=provider,
            region=os.environ.get("AWS_REGION") or os.environ.get("REGION"),
            project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            vault_url=os.environ.get("AZURE_KEY_VAULT_URL"),
            vault_token=os.environ.get("VAULT_TOKEN"),
            timeout=int(os.environ.get("SECRET_TIMEOUT", "30")),
            retry_attempts=int(os.environ.get("SECRET_RETRY_ATTEMPTS", "3")),
            cache_ttl=int(os.environ.get("SECRET_CACHE_TTL", "300")),
        )

        return config

    @staticmethod
    def normalize_secret_name(name: str, provider: SecretProvider) -> str:
        """Normalize secret name according to provider conventions."""
        if provider == SecretProvider.AWS_SECRETS_MANAGER:
            # AWS allows alphanumeric, hyphen, underscore
            return name.replace("/", "-").replace(" ", "_")
        elif provider == SecretProvider.GCP_SECRET_MANAGER:
            # GCP: lowercase letters, numbers, hyphens, underscores
            return name.lower().replace(" ", "-").replace("/", "_")
        elif provider == SecretProvider.AZURE_KEY_VAULT:
            # Azure: alphanumeric, hyphen
            return name.replace("_", "-").replace(" ", "-")
        else:
            return name

    @staticmethod
    def parse_secret_value(value: str, content_type: Optional[str] = None) -> Any:
        """Parse secret value based on content type."""
        if not value:
            return value

        if content_type == "application/json" or value.strip().startswith("{"):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                pass

        # Try to parse as key-value pairs
        if "=" in value and "\n" not in value:
            pairs = value.split(";")
            if len(pairs) > 1:
                result = {}
                for pair in pairs:
                    if "=" in pair:
                        key, val = pair.split("=", 1)
                        result[key.strip()] = val.strip()
                if result:
                    return result

        return value

    @staticmethod
    def validate_secret_name(name: str) -> bool:
        """Validate secret name format."""
        if not name or len(name) > 256:
            return False

        # Basic validation - no special characters except hyphen, underscore, slash
        import re

        pattern = r"^[a-zA-Z0-9_\-/\.]+$"
        return bool(re.match(pattern, name))

    @staticmethod
    def mask_sensitive_data(data: Any, fields: list = None) -> Any:
        """Mask sensitive data in dictionaries or strings."""
        if fields is None:
            fields = ["password", "secret", "key", "token", "credential"]

        if isinstance(data, dict):
            masked = {}
            for key, value in data.items():
                if any(sensitive in key.lower() for sensitive in fields):
                    masked[key] = "***REDACTED***"
                elif isinstance(value, (dict, list)):
                    masked[key] = SecurityClient.mask_sensitive_data(value, fields)
                else:
                    masked[key] = value
            return masked
        elif isinstance(data, list):
            return [SecurityClient.mask_sensitive_data(item, fields) for item in data]
        else:
            return data
