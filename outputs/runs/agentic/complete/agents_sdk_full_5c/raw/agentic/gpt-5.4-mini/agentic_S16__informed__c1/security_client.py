from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from security_models import NormalizedSecret, SecretRequest, SecretResponse, normalize_text


@lru_cache(maxsize=1)
def get_key_vault_url() -> str:
    url = os.environ.get("AZURE_KEY_VAULT_URL") or os.environ.get("AZURE_VAULT_URL")
    if not url:
        raise ValueError("AZURE_KEY_VAULT_URL is required for Azure Key Vault Secrets")
    return url


@lru_cache(maxsize=1)
def get_secret_client() -> SecretClient:
    return SecretClient(vault_url=get_key_vault_url(), credential=DefaultAzureCredential())


def fetch_secret_value(request: SecretRequest) -> SecretResponse:
    client = get_secret_client()
    secret = client.get_secret(request.name, version=request.version_id)
    metadata = {
        "id": getattr(secret, "id", None),
        "enabled": getattr(secret, "properties", None) and getattr(secret.properties, "enabled", None),
        "updated_on": getattr(secret, "properties", None) and getattr(secret.properties, "updated_on", None),
    }
    return SecretResponse(name=request.name, value=normalize_text(secret.value), metadata=metadata)


def fetch_secret_by_stage(name: str, stage: Optional[str] = None) -> NormalizedSecret:
    response = fetch_secret_value(SecretRequest(name=name, version_stage=stage))
    return NormalizedSecret(key=response.name, value=response.value, version=str(response.metadata.get("id") or ""))
