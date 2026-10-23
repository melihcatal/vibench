# Local Secrets Manager configuration helper
# Provides a thin client abstraction for secret storage services
import os
import json
from typing import Dict, Any, TypeVar

# Define generic SecretResponse for use in other modules
SecretResponse = TypeVar('SecretResponse', bound=dict)

class SecretsManagerClient:
    """Abstract client handling secret retrieval for supported providers."

    _PROVIDER = None  # Concrete provider set by subclass

    def __init__(self):
        # Load basic config from env; specifics depend on provider subclass
        self.api_key = os.getenv(self._PROVIDER['auth_key'])
        # Additional init if needed (e.g., endpoint)

    def get_secret_value(self, name: str) -> SecretResponse:
        """Retrieve secret value as dict or raw string depending on provider."""
        raise NotImplementedError("Subclasses must implement get_secret_value")

    def get_secret_version(self, name: str, version: str) -> SecretResponse:
        """Retrieve a specific version or staged value."""
        raise NotImplementedError("Subclasses must implement get_secret_version")

    def get_secret_metadata(self, name: str) -> Dict[str, Any]:
        """Fetch metadata (including labels, notes) for a secret."""
        raise NotImplementedError("Subclasses must implement get_secret_metadata")

    def update_secret_metadata(self, name: str, metadata: Dict[str, Any]):
        """Update secret metadata."""
        raise NotImplementedError("Subclasses must implement update_secret_metadata")