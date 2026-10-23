import os
from typing import Optional
import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from google.cloud import secretmanager

def get_aws_secrets_manager_client():
    """Initializes and returns a Boto3 client for AWS Secrets Manager."""
    # AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN)
    # are expected to be configured in the environment.
    return boto3.client("secretsmanager")

def get_azure_key_vault_client(vault_url: Optional[str] = None) -> SecretClient:
    """Initializes and returns a client for Azure Key Vault."""
    vault_url = vault_url or os.environ.get("AZURE_KEY_VAULT_URL")
    if not vault_url:
        raise ValueError("Azure Key Vault URL must be provided or set in AZURE_KEY_VAULT_URL.")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)

def get_gcp_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    """Initializes and returns a client for Google Cloud Secret Manager."""
    # GOOGLE_APPLICATION_CREDENTIALS should be set in the environment.
    return secretmanager.SecretManagerServiceClient()
