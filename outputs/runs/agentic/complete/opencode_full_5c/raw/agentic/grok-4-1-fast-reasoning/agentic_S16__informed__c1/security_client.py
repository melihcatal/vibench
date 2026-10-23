import os
import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from google.cloud import secretmanager
from ibm_secrets_manager import SecretsManagerV2


def get_aws_secrets_client(region_name=None):
    region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region_name)


def get_azure_keyvault_client(vault_url=None):
    vault_url = vault_url or os.getenv("AZURE_KEY_VAULT_URL")
    return SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())


def get_google_secret_client(project_id=None):
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    return client


def get_ibm_secrets_client(service_url=None):
    service_url = service_url or os.getenv("IBM_SECRETS_MANAGER_SERVICE_URL")
    apikey = os.getenv("IBM_SECRETS_MANAGER_APIKEY")
    client = SecretsManagerV2.new_instance()
    client.set_service_url(service_url)
    client.set_api_key(apikey)
    return client
