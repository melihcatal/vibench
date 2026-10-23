import os
from typing import Optional

def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
    return os.getenv(key, default)

def get_aws_secretsmanager_client():
    import boto3
    return boto3.client('secretsmanager')

def get_gcp_secretmanager_client():
    from google.cloud import secretmanager
    return secretmanager.SecretManagerServiceClient()

def get_gcp_project() -> str:
    project = get_env('GOOGLE_CLOUD_PROJECT')
    if not project:
        raise ValueError('GOOGLE_CLOUD_PROJECT environment variable required')
    return project

def get_azure_keyvault_client(vault_url: Optional[str] = None):
    from azure.keyvault.secrets import SecretClient
    from azure.identity import DefaultAzureCredential
    if vault_url is None:
        vault_url = get_env('AZURE_KEYVAULT_URL')
        if not vault_url:
            raise ValueError('AZURE_KEYVAULT_URL environment variable required')
    return SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())