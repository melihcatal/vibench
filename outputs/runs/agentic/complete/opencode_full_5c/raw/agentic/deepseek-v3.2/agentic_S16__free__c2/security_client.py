import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SecretConfig:
    """Configuration for secret management."""

    region: str = "us-east-1"
    max_retries: int = 3
    timeout: int = 30
    cache_ttl: int = 300  # 5 minutes
    use_local_cache: bool = True


class SecurityClient:
    """Client helper utilities for Secret Management."""

    def __init__(self, config: Optional[SecretConfig] = None):
        self.config = config or SecretConfig()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[str, float] = {}

    @staticmethod
    def load_config_from_env() -> SecretConfig:
        """Load configuration from environment variables."""
        return SecretConfig(
            region=os.environ.get("AWS_REGION", "us-east-1"),
            max_retries=int(os.environ.get("SECRET_MAX_RETRIES", "3")),
            timeout=int(os.environ.get("SECRET_TIMEOUT", "30")),
            cache_ttl=int(os.environ.get("SECRET_CACHE_TTL", "300")),
            use_local_cache=os.environ.get("SECRET_USE_CACHE", "true").lower()
            == "true",
        )

    def get_cached_secret(self, secret_name: str) -> Optional[Dict[str, Any]]:
        """Get secret from local cache if valid."""
        import time

        if not self.config.use_local_cache:
            return None

        if secret_name in self._cache:
            cache_time = self._cache_timestamps.get(secret_name, 0)
            current_time = time.time()

            if current_time - cache_time < self.config.cache_ttl:
                return self._cache[secret_name]

        return None

    def cache_secret(self, secret_name: str, secret_data: Dict[str, Any]) -> None:
        """Cache secret data locally."""
        import time

        if self.config.use_local_cache:
            self._cache[secret_name] = secret_data
            self._cache_timestamps[secret_name] = time.time()

    def clear_cache(self, secret_name: Optional[str] = None) -> None:
        """Clear cache for a specific secret or all secrets."""
        if secret_name:
            if secret_name in self._cache:
                del self._cache[secret_name]
            if secret_name in self._cache_timestamps:
                del self._cache_timestamps[secret_name]
        else:
            self._cache.clear()
            self._cache_timestamps.clear()

    @staticmethod
    def normalize_secret_name(secret_name: str) -> str:
        """Normalize secret name to ensure consistency."""
        # Remove leading/trailing slashes and normalize path
        normalized = secret_name.strip("/")
        # Replace multiple slashes with single slash
        while "//" in normalized:
            normalized = normalized.replace("//", "/")
        return normalized

    @staticmethod
    def validate_secret_name(secret_name: str) -> bool:
        """Validate secret name format."""
        if not secret_name or len(secret_name) > 256:
            return False

        # AWS Secrets Manager naming constraints
        invalid_chars = set("\"'\\|{}[]()<>*?&^%$#@!~`")
        if any(char in secret_name for char in invalid_chars):
            return False

        return True

    @staticmethod
    def mask_sensitive_data(data: Any, fields_to_mask: list = None) -> Any:
        """Mask sensitive data in logs or responses."""
        if fields_to_mask is None:
            fields_to_mask = ["password", "secret", "key", "token", "credential"]

        if isinstance(data, dict):
            masked = {}
            for key, value in data.items():
                if any(mask_word in key.lower() for mask_word in fields_to_mask):
                    masked[key] = "***MASKED***"
                else:
                    masked[key] = SecurityClient.mask_sensitive_data(
                        value, fields_to_mask
                    )
            return masked
        elif isinstance(data, list):
            return [
                SecurityClient.mask_sensitive_data(item, fields_to_mask)
                for item in data
            ]
        else:
            return data
