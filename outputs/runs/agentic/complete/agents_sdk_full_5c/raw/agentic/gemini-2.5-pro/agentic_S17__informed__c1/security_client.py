# security_client.py
import os
import boto3
from google.cloud import kms_v1
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

def get_aws_kms_client():
    """Initializes and returns a Boto3 KMS client."""
    return boto3.client(
        "kms",
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

def get_gcp_kms_client():
    """Initializes and returns a Google Cloud KMS client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS is set in the environment
    return kms_v1.KeyManagementServiceClient()

def get_azure_key_client():
    """Initializes and returns an Azure Key Vault KeyClient."""
    key_vault_url = os.environ.get("AZURE_KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("AZURE_KEY_VAULT_URL environment variable not set.")
    credential = DefaultAzureCredential()
    return KeyClient(vault_url=key_vault_url, credential=credential)
