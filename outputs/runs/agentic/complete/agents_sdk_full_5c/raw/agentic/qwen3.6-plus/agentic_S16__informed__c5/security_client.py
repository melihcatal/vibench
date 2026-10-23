"""Local configuration and client helper utilities for Secret Management.

Provides shared helpers for loading provider configuration, building client
instances, and normalizing secret payloads across different secret backends.
"""

import os
import json
from typing import Any


class SecretProviderConfig:
    """Holds configuration for a specific secret provider."""

    def __init__(
        self,
        provider: str,
        region: str | None = None,
        vault_url: str | None = None,
        project_id: str | None = None,
        extra: dict[str, Any] | None = None,
    ):
        self.provider = provider
        self.region = region
        self.vault_url = vault_url
        self.project_id = project_id
        self.extra = extra or {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "region": self.region,
            "vault_url": self.vault_url,
            "project_id": self.project_id,
            "extra": self.extra,
        }


def load_provider_config(provider: str) -> SecretProviderConfig:
    """Load configuration for the given secret provider from environment variables.

    Supported providers: aws, azure, gcp, doppler, alibaba, ibm.
    """
    provider = provider.lower()
    if provider == "aws":
        return SecretProviderConfig(
            provider="aws",
            region=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        )
    if provider == "azure":
        return SecretProviderConfig(
            provider="azure",
            vault_url=os.environ.get("AZURE_KEY_VAULT_URL"),
        )
    if provider == "gcp":
        return SecretProviderConfig(
            provider="gcp",
            project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        )
    if provider == "doppler":
        return SecretProviderConfig(
            provider="doppler",
            extra={
                "project": os.environ.get("DOPPLER_PROJECT"),
                "config": os.environ.get("DOPPLER_CONFIG", "prod"),
            },
        )
    if provider == "alibaba":
        return SecretProviderConfig(
            provider="alibaba",
            region=os.environ.get("ALIBABA_CLOUD_REGION", "cn-hangzhou"),
        )
    if provider == "ibm":
        return SecretProviderConfig(
            provider="ibm",
            extra={
                "url": os.environ.get("IBM_SECRETS_MANAGER_URL"),
                "instance_id": os.environ.get("IBM_SECRETS_MANAGER_INSTANCE_ID"),
            },
        )
    raise ValueError(f"Unsupported secret provider: {provider}")


def normalize_secret_payload(raw: str) -> dict[str, Any]:
    """Normalize a raw secret string into a consistent dictionary structure.

    Attempts JSON parsing first, then falls back to key=value splitting,
    and finally returns a raw-only structure.
    """
    raw = raw.strip()
    if not raw:
        return {"raw": "", "parsed": {}}

    # Try JSON
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict):
            return {"raw": raw, "parsed": parsed, "format": "json"}
    except (json.JSONDecodeError, TypeError):
        pass

    # Try key=value pairs (semicolon or newline separated)
    parsed: dict[str, str] = {}
    separators = [";", "\n", "&"]
    for sep in separators:
        if sep in raw:
            for token in raw.split(sep):
                token = token.strip()
                if "=" in token:
                    k, v = token.split("=", 1)
                    parsed[k.strip().lower()] = v.strip()
            if parsed:
                return {"raw": raw, "parsed": parsed, "format": "key_value"}

    return {"raw": raw, "parsed": {}, "format": "opaque"}


def mask_secret_value(value: str, visible: int = 4) -> str:
    """Mask a secret value, showing only the last `visible` characters."""
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]
