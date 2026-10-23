from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

from security_models import NormalizedSecret, SecretRequest, normalize_secret_payload, prefer_first

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@lru_cache(maxsize=1)
def get_key_vault_url() -> str:
    url = os.environ.get("AZURE_KEY_VAULT_URL") or os.environ.get("AZURE_VAULT_URL")
    if not url:
        raise EnvironmentError("AZURE_KEY_VAULT_URL is required for Azure Key Vault Secrets")
    return url


@lru_cache(maxsize=1)
def get_secret_client() -> SecretClient:
    return SecretClient(vault_url=get_key_vault_url(), credential=DefaultAzureCredential())


def fetch_secret(request: SecretRequest) -> NormalizedSecret:
    client = get_secret_client()
    kwargs: Dict[str, Any] = {}
    if request.version_id:
        kwargs["version"] = request.version_id
    try:
        secret = client.get_secret(request.secret_name, **kwargs)
    except ResourceNotFoundError:
        if request.version_stage:
            secret = client.get_secret(request.secret_name, version=request.version_stage)
        else:
            raise
    return normalize_secret_payload(
        name=secret.name,
        value=secret.value,
        metadata={
            "id": prefer_first(secret.properties.__dict__, ["id"], None),
            "enabled": getattr(secret.properties, "enabled", None),
            "created_on": getattr(secret.properties, "created_on", None),
            "updated_on": getattr(secret.properties, "updated_on", None),
            "tags": getattr(secret.properties, "tags", None),
        },
    )


def fetch_secret_value(secret_name: str, version_id: Optional[str] = None, version_stage: Optional[str] = None) -> str:
    return fetch_secret(SecretRequest(secret_name=secret_name, version_id=version_id, version_stage=version_stage)).value
