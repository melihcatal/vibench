from typing import Optional, Dict, Any
import os
from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import boto3


class SecretManagerClient:
    """Provides a unified interface for interacting with secret management services."""

    def __init__(self, provider: str, **kwargs):
        self.provider = provider
        self.client = self._initialize_client(**kwargs)

    def _initialize_client(self, **kwargs) -> Any:
        if self.provider == "google":
            return secretmanager.SecretManagerServiceClient()
        elif self.provider == "azure":
            return SecretClient(vault_url=kwargs["vault_url"], credential=DefaultAzureCredential())
        elif self.provider == "aws":
            return boto3.client("secretsmanager", region_name=kwargs["region_name"])
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def get_secret(self, secret_id: str, **kwargs) -> str:
        if self.provider == "google":
            name = f"projects/{kwargs['project_id']}/secrets/{secret_id}/versions/{kwargs.get('version_id', 'latest')}"
            response = self.client.access_secret_version(request={"name": name})
            return response.payload.data.decode("UTF-8")
        elif self.provider == "azure":
            secret = self.client.get_secret(secret_id, kwargs.get("version"))
            return secret.value
        elif self.provider == "aws":
            response = self.client.get_secret_value(SecretId=secret_id)
            return response["SecretString"]
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")