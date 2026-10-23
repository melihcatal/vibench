import os
import boto3
from google.cloud import secretmanager_v1beta1 as secretmanager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_aws_secrets_manager_client(region_name: str = None):
    """
    Returns an AWS Secrets Manager client.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region_name)

def get_google_secret_manager_client():
    """
    Returns a Google Secret Manager client.
    """
    return secretmanager.SecretManagerServiceClient()

def get_azure_key_vault_secret_client(vault_url: str):
    """
    Returns an Azure Key Vault SecretClient.
    """
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)
