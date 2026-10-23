import os
from typing import Any

import boto3
from google.cloud import secretmanager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_aws_secrets_manager_client() -> Any:
    return boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_google_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()

def get_azure_key_vault_secret_client(vault_url: str) -> SecretClient:
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)
