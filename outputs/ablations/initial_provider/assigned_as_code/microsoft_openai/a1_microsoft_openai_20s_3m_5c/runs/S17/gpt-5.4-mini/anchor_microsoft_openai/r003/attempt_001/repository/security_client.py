import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.keys.crypto import CryptographyClient


def get_keyvault_client(key_id=None):
    key_id = key_id or os.environ.get('AZURE_KEY_VAULT_KEY_ID')
    if not key_id:
        raise ValueError('AZURE_KEY_VAULT_KEY_ID is required')
    return CryptographyClient(key_id, credential=DefaultAzureCredential())


def get_security_config(overrides=None):
    overrides = overrides or {}
    config = {'key_id': os.environ.get('AZURE_KEY_VAULT_KEY_ID')}
    config.update({k: v for k, v in overrides.items() if v is not None})
    return config
