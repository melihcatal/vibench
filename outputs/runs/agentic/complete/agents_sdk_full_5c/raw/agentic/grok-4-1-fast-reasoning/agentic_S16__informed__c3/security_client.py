import os
import boto3
from google.cloud import secretmanager
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import requests
from typing import Optional

def get_aws_secrets_client(region: Optional[str] = None) -> 'boto3.client':
    region = region or os.getenv('AWS_REGION', 'us-east-1')
    return boto3.client(
        'secretsmanager',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=region
    )

def get_google_secret_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()

def get_azure_keyvault_client(vault_url: Optional[str] = None) -> SecretClient:
    vault_url = vault_url or os.getenv('AZURE_KEY_VAULT_URL')
    if not vault_url:
        raise ValueError('AZURE_KEY_VAULT_URL must be set')
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)

def get_doppler_client() -> requests.Session:
    token = os.getenv('DOPPLER_TOKEN')
    if not token:
        raise ValueError('DOPPLER_TOKEN must be set')
    session = requests.Session()
    session.headers.update({'Authorization': f'Token token={token}'})
    return session
