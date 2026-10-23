import os

from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import boto3

def get_gcp_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()

def get_azure_key_vault_secret_client(vault_url: str):
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)

def get_aws_secrets_manager_client():
    return boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
