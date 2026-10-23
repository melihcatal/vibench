import os
import json
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class SecretProvider(Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    VAULT = "vault"


@dataclass
class SecretConfig:
    provider: SecretProvider
    secret_name: str
    project_id: Optional[str] = None
    vault_path: Optional[str] = None
    key_vault_name: Optional[str] = None
    version: Optional[str] = None


class SecurityClient:
    """Local configuration and client helper utilities for Secret Management."""

    def __init__(self, config_file: str = "security_config.json"):
        self.config = self._load_config(config_file)
        self._clients = {}

    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load security configuration from file."""
        config_path = os.path.join(os.path.dirname(__file__), config_file)

        if not os.path.exists(config_path):
            return {
                "default_provider": os.environ.get("SECRET_PROVIDER", "aws"),
                "providers": {},
            }

        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Error loading security config: {e}")

    def get_provider_config(self, provider: SecretProvider) -> Dict[str, Any]:
        """Get configuration for a specific provider."""
        provider_key = provider.value
        if provider_key in self.config.get("providers", {}):
            return self.config["providers"][provider_key]
        return {}

    def normalize_secret_response(
        self, provider: SecretProvider, raw_response: Any
    ) -> Dict[str, Any]:
        """Normalize secret response from different providers."""
        if provider == SecretProvider.AWS:
            if isinstance(raw_response, str):
                try:
                    return json.loads(raw_response)
                except json.JSONDecodeError:
                    return {"value": raw_response}
            elif isinstance(raw_response, dict):
                return raw_response
            else:
                return {"value": str(raw_response)}

        elif provider == SecretProvider.GCP:
            if isinstance(raw_response, dict):
                return raw_response
            elif isinstance(raw_response, str):
                try:
                    return json.loads(raw_response)
                except json.JSONDecodeError:
                    return {"value": raw_response}
            else:
                return {"value": str(raw_response)}

        elif provider == SecretProvider.AZURE:
            if isinstance(raw_response, str):
                try:
                    return json.loads(raw_response)
                except json.JSONDecodeError:
                    return {"value": raw_response}
            else:
                return {"value": str(raw_response)}

        elif provider == SecretProvider.VAULT:
            if isinstance(raw_response, dict):
                return raw_response
            elif isinstance(raw_response, str):
                try:
                    return json.loads(raw_response)
                except json.JSONDecodeError:
                    return {"value": raw_response}
            else:
                return {"value": str(raw_response)}

        return {"value": str(raw_response)}

    def validate_secret_structure(
        self, secret_data: Dict[str, Any], expected_fields: list
    ) -> bool:
        """Validate that secret data contains expected fields."""
        if not isinstance(secret_data, dict):
            return False

        for field in expected_fields:
            if field not in secret_data:
                return False

        return True

    def mask_sensitive_data(
        self, data: Dict[str, Any], sensitive_fields: list = None
    ) -> Dict[str, Any]:
        """Mask sensitive data in logs or outputs."""
        if sensitive_fields is None:
            sensitive_fields = ["password", "token", "key", "secret", "credential"]

        masked_data = data.copy()
        for key in masked_data:
            if any(sensitive in key.lower() for sensitive in sensitive_fields):
                if isinstance(masked_data[key], str) and len(masked_data[key]) > 4:
                    masked_data[key] = (
                        masked_data[key][:2] + "***" + masked_data[key][-2:]
                    )
                else:
                    masked_data[key] = "***"

        return masked_data
