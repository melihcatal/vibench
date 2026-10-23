from typing import Optional
import os
from google.cloud import secretmanager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import boto3


class GoogleSecretManagerClient:
    """Helper client for Google Cloud Secret Manager."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.client = secretmanager.SecretManagerServiceClient()

    def get_secret(self, secret_id: str, version_id: str = "latest") -> str:
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")


class AzureKeyVaultClient:
    """Helper client for Azure Key Vault."""

    def __init__(self, vault_url: Optional[str] = None):
        self.vault_url = vault_url or os.getenv("AZURE_KEY_VAULT_URL")
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_name: str) -> str:
        secret = self.client.get_secret(secret_name)
        return secret.value


class AWSSecretsManagerClient:
    """Helper client for AWS Secrets Manager."""

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION")
        self.client = boto3.client(service_name="secretsmanager", region_name=self.region_name)

    def get_secret(self, secret_name: str) -> str:
        response = self.client.get_secret_value(SecretId=secret_name)
        return response["SecretString"]