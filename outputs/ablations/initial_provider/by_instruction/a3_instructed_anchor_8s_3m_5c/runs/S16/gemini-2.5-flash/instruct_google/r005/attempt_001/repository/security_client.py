from google.cloud import secretmanager
import boto3
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_google_secret_manager_client():
    """
    Returns a Google Secret Manager client.
    """
    return secretmanager.SecretManagerServiceClient()

def get_aws_secrets_manager_client(region_name: str = "us-east-1"):
    """
    Returns an AWS Secrets Manager client.
    """
    return boto3.client("secretsmanager", region_name=region_name)

def get_azure_key_vault_secret_client(key_vault_name: str):
    """
    Returns an Azure Key Vault Secret client.
    """
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=key_vault_uri, credential=credential)
