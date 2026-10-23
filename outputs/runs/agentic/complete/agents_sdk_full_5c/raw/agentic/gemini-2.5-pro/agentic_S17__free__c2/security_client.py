import os
import boto3
from google.cloud import kms
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient
from azure.identity import DefaultAzureCredential
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
import openai
import cohere
import deepl

def get_aws_kms_client():
    """Returns an AWS KMS client."""
    return boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_gcp_kms_client():
    """Returns a Google Cloud KMS client."""
    return kms.KeyManagementServiceClient()

def get_azure_crypto_client(key_name: str):
    """Returns an Azure Key Vault Cryptography client for a specific key."""
    key_vault_name = os.environ.get("AZURE_KEY_VAULT_NAME")
    kv_uri = f"https://{key_vault_name}.vault.azure.net"
    credential = DefaultAzureCredential()
    key_client = KeyClient(vault_url=kv_uri, credential=credential)
    key = key_client.get_key(key_name)
    return CryptographyClient(key.id, credential)

def get_datadog_logs_api():
    """Returns a Datadog Logs API client."""
    configuration = Configuration()
    api_client = ApiClient(configuration)
    return LogsApi(api_client)

def get_openai_client():
    """Returns an OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

def get_cohere_client():
    """Returns a Cohere client."""
    api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(api_key)

def get_deepl_translator():
    """Returns a DeepL Translator client."""
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    return deepl.Translator(auth_key)
