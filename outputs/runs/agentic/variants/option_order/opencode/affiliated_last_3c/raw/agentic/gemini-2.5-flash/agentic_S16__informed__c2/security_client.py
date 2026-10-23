import os
from google.cloud import secretmanager_v1 as secretmanager
import boto3
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from ibm_secrets_manager_sdk.secrets_manager_v2 import *  # type: ignore
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator  # type: ignore


def get_google_secret_manager_client():
    """Returns a Google Secret Manager client."""
    return secretmanager.SecretManagerServiceClient()


def get_aws_secrets_manager_client():
    """Returns an AWS Secrets Manager client."""
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region_name)


def get_azure_key_vault_secret_client(vault_url: str | None = None):
    """Returns an Azure Key Vault SecretClient."""
    if not vault_url:
        vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
        if not vault_url:
            raise ValueError(
                "AZURE_KEY_VAULT_URL environment variable not set or vault_url not provided."
            )
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)


def get_ibm_secrets_manager_client():
    """Returns an IBM Cloud Secrets Manager client."""
    api_key = os.environ.get("IBM_SECRETS_MANAGER_APIKEY")
    service_url = os.environ.get("IBM_SECRETS_MANAGER_URL")
    if not api_key or not service_url:
        raise ValueError(
            "IBM_SECRETS_MANAGER_APIKEY and IBM_SECRETS_MANAGER_URL environment variables must be set."
        )

    authenticator = IAMAuthenticator(api_key)
    secrets_manager_service = SecretsManagerV2(authenticator=authenticator)
    secrets_manager_service.set_service_url(service_url)
    return secrets_manager_service
