import os
import boto3
import hvac
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from google.cloud import secretmanager

def get_aws_secrets_manager_client(region_name: str = None):
    """
    Returns an AWS Secrets Manager client.
    """
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region_name)

def get_gcp_secret_manager_client():
    """
    Returns a Google Secret Manager client.
    """
    return secretmanager.SecretManagerServiceClient()

def get_azure_key_vault_secret_client(key_vault_name: str):
    """
    Returns an Azure Key Vault SecretClient.
    """
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=key_vault_uri, credential=credential)

def get_hashicorp_vault_client(vault_address: str = None, token: str = None):
    """
    Returns a HashiCorp Vault client.
    """
    if vault_address is None:
        vault_address = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
    if token is None:
        token = os.environ.get("VAULT_TOKEN")
    
    if not token:
        raise ValueError("VAULT_TOKEN must be provided or set as an environment variable for HashiCorp Vault.")

    return hvac.Client(url=vault_address, token=token)
