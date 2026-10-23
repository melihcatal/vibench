import os
import boto3
from google.cloud import secretmanager
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import hvac


def get_aws_secrets_manager_client():
    return boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION"))


def get_gcp_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()


def get_azure_key_vault_client():
    vault_url = os.environ.get("AZURE_VAULT_URL")
    if not vault_url:
        raise ValueError("AZURE_VAULT_URL environment variable not set.")
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)


def get_hvac_client():
    vault_addr = os.environ.get("VAULT_ADDR")
    vault_token = os.environ.get("VAULT_TOKEN")
    if not vault_addr:
        raise ValueError("VAULT_ADDR environment variable not set.")
    return hvac.Client(url=vault_addr, token=vault_token)
