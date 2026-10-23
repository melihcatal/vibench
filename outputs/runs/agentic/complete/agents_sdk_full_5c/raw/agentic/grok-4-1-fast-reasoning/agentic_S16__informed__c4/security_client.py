import os
from typing import Dict, Any

def get_aws_region() -> str:
    return os.getenv('AWS_REGION', 'us-east-1')

def get_azure_vault_url() -> str:
    return os.getenv('AZURE_KEY_VAULT_URL')

def get_google_project() -> str:
    return os.getenv('GOOGLE_CLOUD_PROJECT')

def get_doppler_token() -> str:
    return os.getenv('DOPPLER_TOKEN')

def get_doppler_config() -> str:
    return os.getenv('DOPPLER_CONFIG', 'default-config')
