import os
from dataclasses import dataclass
from typing import Any, Optional

# Provider-specific client imports for managed secret services
from google.cloud import secretmanager as gcp_secretmanager
import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import hvac


@dataclass
class ClientConfig:
    provider: str = os.getenv("SECRET_PROVIDER", "gcp")
    project_id: Optional[str] = os.getenv("GOOGLE_CLOUD_PROJECT")
    region_name: Optional[str] = os.getenv("AWS_REGION")
    vault_url: Optional[str] = os.getenv("VAULT_ADDR")


def get_secret_manager_client(provider: Optional[str] = None, **kwargs: Any):
    selected = (provider or os.getenv("SECRET_PROVIDER") or "gcp").lower()
    if selected in {"gcp", "google", "google_cloud"}:
        return gcp_secretmanager.SecretManagerServiceClient()
    if selected in {"aws", "secretsmanager"}:
        region_name = kwargs.get("region_name") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
        return boto3.client("secretsmanager", region_name=region_name)
    if selected in {"azure", "keyvault", "key_vault"}:
        vault_url = kwargs.get("vault_url") or os.getenv("AZURE_KEY_VAULT_URL")
        return SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
    if selected in {"vault", "hashicorp"}:
        return hvac.Client(url=kwargs.get("url") or os.getenv("VAULT_ADDR"), token=os.getenv("VAULT_TOKEN"))
    raise ValueError(f"Unsupported secret provider: {selected}")


def get_secret_name(project_id: Optional[str], secret_id: str) -> str:
    if project_id:
        return f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    return secret_id
