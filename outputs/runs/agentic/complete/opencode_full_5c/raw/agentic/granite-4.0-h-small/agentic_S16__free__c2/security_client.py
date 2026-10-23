# security_client.py
# [HELPER] Local configuration and client helper utilities for Secret Management

import os
from typing import Any, Dict

# Example: load provider-specific credentials from environment variables
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AZURE_TENANT = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT = os.getenv("AZURE_CLIENT_ID")
AZURE_SECRET = os.getenv("AZURE_CLIENT_SECRET")
GOOGLE_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
GOOGLE_SA_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# ---------------------------------------------------------------------------
# Helper to instantiate the appropriate secret manager client based on env
# ---------------------------------------------------------------------------
def get_secret_manager_client(provider: str = "aws") -> Any:
    """Return a secret manager client for the requested provider.

    Args:
        provider: 'aws', 'azure', or 'gcp'.

    Returns:
        Configured client instance.
    """
    if provider == "aws":
        import boto3

        return boto3.client(
            "secretsmanager",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
    elif provider == "azure":
        from azure.identity import DefaultAzureCredential
        from azure.keyvault.secrets import SecretClient

        credential = DefaultAzureCredential()
        vault_url = os.getenv("AZURE_KEYVAULT_URL")
        return SecretClient(vault_url=vault_url, credential=credential)
    elif provider == "gcp":
        from google.cloud import secretmanager

        return secretmanager.SecretManagerServiceClient()
    else:
        raise ValueError(f"Unsupported provider: {provider}")
