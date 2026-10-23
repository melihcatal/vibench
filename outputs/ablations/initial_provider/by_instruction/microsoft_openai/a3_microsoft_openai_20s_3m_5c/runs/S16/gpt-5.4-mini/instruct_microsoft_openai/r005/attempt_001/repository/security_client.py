import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


@dataclass
class SecurityClientConfig:
    vault_url: str
    azure_tenant_id: Optional[str] = None


def load_security_config() -> SecurityClientConfig:
    vault_url = os.environ.get("AZURE_KEY_VAULT_URL", "")
    if not vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL is required")
    return SecurityClientConfig(vault_url=vault_url, azure_tenant_id=os.environ.get("AZURE_TENANT_ID"))


def create_secret_client(config: Optional[SecurityClientConfig] = None) -> SecretClient:
    cfg = config or load_security_config()
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=cfg.vault_url, credential=credential)


def get_secret_value(name: str, version: Optional[str] = None, config: Optional[SecurityClientConfig] = None) -> str:
    client = create_secret_client(config)
    secret = client.get_secret(name, version=version)
    return secret.value


def normalize_secret_payload(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"value": payload}
