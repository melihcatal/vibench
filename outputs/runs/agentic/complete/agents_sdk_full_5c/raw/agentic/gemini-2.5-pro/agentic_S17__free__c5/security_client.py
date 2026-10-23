import os
import boto3
from google.cloud import kms_v1
from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient
import datadog_api_client
from deepl import Translator
import cohere
import googleapiclient.discovery


def get_aws_kms_client() -> boto3.client:
    """Initializes and returns a Boto3 client for AWS KMS."""
    return boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )


def get_google_kms_client() -> kms_v1.KeyManagementServiceClient:
    """Initializes and returns a client for Google Cloud KMS."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return kms_v1.KeyManagementServiceClient()


def get_azure_key_vault_crypto_client() -> CryptographyClient:
    """Initializes and returns a crypto client for an Azure Key Vault key."""
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    key_name = os.environ.get("AZURE_KEY_NAME")
    if not key_vault_url or not key_name:
        raise ValueError("Azure Key Vault environment variables not set.")

    key_identifier = f"{key_vault_url}/keys/{key_name}"
    credential = DefaultAzureCredential()
    return CryptographyClient(key_identifier, credential)


def get_datadog_api_client():
    """Returns an initialized Datadog API client."""
    configuration = datadog_api_client.Configuration(
        api_key={
            "apiKeyAuth": os.environ.get("DATADOG_API_KEY"),
            "appKeyAuth": os.environ.get("DATADOG_APP_KEY"),
        }
    )
    api_client = datadog_api_client.ApiClient(configuration)
    return api_client


def get_deepl_translator() -> Translator:
    """Returns an initialized DeepL Translator client."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")
    return Translator(auth_key)
    
def get_cohere_client() -> cohere.Client:
    """Initializes and returns a Cohere client."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY not set")
    return cohere.Client(api_key)

def get_perspective_api_client():
    """Initializes and returns a client for the Google Perspective API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    
    return googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )
