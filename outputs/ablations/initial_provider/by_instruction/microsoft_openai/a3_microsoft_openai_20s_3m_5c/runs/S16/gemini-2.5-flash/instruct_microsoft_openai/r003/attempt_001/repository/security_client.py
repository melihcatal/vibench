import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_azure_key_vault_client(vault_url: str) -> SecretClient:
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    return client

def get_aws_secrets_manager_client():
    import boto3
    return boto3.client('secretsmanager')

def get_google_secret_manager_client():
    from google.cloud import secretmanager
    return secretmanager.SecretManagerServiceClient()

def get_hashicorp_vault_client(vault_address: str, token: str):
    import hvac
    client = hvac.Client(url=vault_address, token=token)
    return client

def get_openai_client():
    from openai import OpenAI
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return OpenAI(api_key=api_key)
