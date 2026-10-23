import os

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def load_security_config(config=None):
    config = config or {}
    vault_url = config.get('vault_url') or os.environ['AZURE_KEYVAULT_URL']
    return {'vault_url': vault_url}


def build_secret_client(config=None):
    loaded = load_security_config(config)
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=loaded['vault_url'], credential=credential), credential


def close_client(client, credential=None):
    if client is not None:
        client.close()
    if credential is not None:
        credential.close()
