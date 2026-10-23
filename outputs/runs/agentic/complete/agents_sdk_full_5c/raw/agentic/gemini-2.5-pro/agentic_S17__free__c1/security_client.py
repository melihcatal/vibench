
import os
import boto3
from google.cloud import kms_v1
from azure.keyvault.keys.crypto import CryptographyClient
from azure.identity import DefaultAzureCredential

_aws_kms_client = None
_google_kms_client = None
_azure_crypto_clients = {}

def get_aws_kms_client():
    """Initializes and returns a boto3 KMS client."""
    global _aws_kms_client
    if _aws_kms_client is None:
        _aws_kms_client = boto3.client(
            "kms",
            region_name=os.environ.get("AWS_REGION", "us-east-1")
        )
    return _aws_kms_client

def get_google_kms_client():
    """Initializes and returns a Google Cloud KMS client."""
    global _google_kms_client
    if _google_kms_client is None:
        _google_kms_client = kms_v1.KeyManagementServiceClient()
    return _google_kms_client

def get_azure_crypto_client(key_id: str) -> CryptographyClient:
    """
    Initializes and returns an Azure Key Vault CryptographyClient.
    key_id should be the full key identifier URL from Key Vault.
    """
    global _azure_crypto_clients
    if key_id not in _azure_crypto_clients:
        credential = DefaultAzureCredential()
        _azure_crypto_clients[key_id] = CryptographyClient(key_id, credential)
    return _azure_crypto_clients[key_id]
