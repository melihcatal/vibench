from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from security_models import SecretRequest


@dataclass
class SecurityClientConfig:
    provider: str = "azure-key-vault-secrets"
    secret_store_url: Optional[str] = None
    region: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SecurityClientConfig":
        return cls(
            secret_store_url=os.getenv("AZURE_KEY_VAULT_URL") or os.getenv("AZURE_VAULT_URL"),
            region=os.getenv("AZURE_REGION"),
        )


def build_secret_request(secret_id: str, version_id: Optional[str] = None, stage: Optional[str] = None) -> SecretRequest:
    return SecretRequest(secret_id=secret_id, version_id=version_id, stage=stage)


def load_secret_name(default: str) -> str:
    return os.getenv("SECRET_NAME", default)


def require_setting(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing required setting: {name}")
    return value


def create_provider_hint() -> str:
    return "Azure Key Vault Secrets"


def safe_dict(payload: Any) -> dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"value": payload}
