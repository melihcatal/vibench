import os
import boto3
from google.cloud import kms
from azure.keyvault.keys.crypto import KeyVaultCryptoClient
from azure.identity import DefaultAzureCredential
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from googleapiclient import discovery
import cohere
import deepl

def get_aws_kms_client():
    """Provides a boto3 client for AWS KMS."""
    return boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_gcp_kms_client():
    """Provides a client for Google Cloud KMS."""
    return kms.KeyManagementServiceClient()

def get_azure_crypto_client(key_vault_uri: str):
    """Provides a client for Azure Key Vault crypto operations."""
    credential = DefaultAzureCredential()
    return KeyVaultCryptoClient(vault_url=key_vault_uri, credential=credential)

def get_datadog_logs_api():
    """Provides a client for the Datadog Logs API."""
    configuration = Configuration()
    api_client = ApiClient(configuration)
    return LogsApi(api_client)

def get_perspective_api_client():
    """Provides a client for the Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

def get_cohere_client():
    """Provides a client for the Cohere API."""
    cohere_api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(cohere_api_key)

def get_deepl_translator():
    """Provides a client for the DeepL API."""
    deepl_auth_key = os.environ.get("DEEPL_AUTH_KEY")
    return deepl.Translator(deepl_auth_key)
