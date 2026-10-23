import os
import boto3
from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import hvac


def get_aws_secretsmanager_client():
    region_name = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region_name)


def get_gcp_project_id():
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable is required")
    return project_id


def get_gcp_secretmanager_client():
    return secretmanager.SecretManagerServiceClient()


def get_azure_keyvault_client():
    vault_url = os.getenv("AZURE_KEYVAULT_URL")
    if not vault_url:
        raise ValueError("AZURE_KEYVAULT_URL environment variable is required")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)


def get_vault_client():
    vault_addr = os.getenv("VAULT_ADDR")
    vault_token = os.getenv("VAULT_TOKEN")
    if not vault_addr or not vault_token:
        raise ValueError(
            "VAULT_ADDR and VAULT_TOKEN environment variables are required"
        )
    client = hvac.Client(url=vault_addr)
    client.token = vault_token
    client.is_authenticated()
    return client
