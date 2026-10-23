import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def load_config(config=None):
    config = dict(config or {})
    if 'vault_url' not in config:
        config['vault_url'] = os.environ['AZURE_KEYVAULT_URL']
    return config


def build_secret_client(config=None):
    config = load_config(config)
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=config['vault_url'], credential=credential)


def get_secret_value(secret_id, config=None):
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=load_config(config)['vault_url'], credential=credential) as client:
            return client.get_secret(secret_id).value
