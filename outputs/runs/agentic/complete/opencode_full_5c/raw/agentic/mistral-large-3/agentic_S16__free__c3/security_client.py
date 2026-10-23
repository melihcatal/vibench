from typing import Optional
import os
from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import boto3


class GoogleSecretManagerClient:
    """Client helper for Google Cloud Secret Manager."""

    def __init__(self, project_id: Optional[str] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.client = secretmanager.SecretManagerServiceClient()


class AzureKeyVaultClient:
    """Client helper for Azure Key Vault."""

    def __init__(self, key_vault_name: Optional[str] = None):
        self.key_vault_name = key_vault_name or os.getenv("AZURE_KEY_VAULT_NAME")
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(
            vault_url=f"https://{self.key_vault_name}.vault.azure.net",
            credential=self.credential,
        )


class AWSSecretsManagerClient:
    """Client helper for AWS Secrets Manager."""

    def __init__(self, region_name: Optional[str] = None):
        self.region_name = region_name or os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        self.client = boto3.client("secretsmanager", region_name=self.region_name)


def load_config():
    """Loads configuration from environment variables."""
    return {
        "google_cloud_project": os.getenv("GOOGLE_CLOUD_PROJECT"),
        "azure_key_vault_name": os.getenv("AZURE_KEY_VAULT_NAME"),
        "aws_region": os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    }
