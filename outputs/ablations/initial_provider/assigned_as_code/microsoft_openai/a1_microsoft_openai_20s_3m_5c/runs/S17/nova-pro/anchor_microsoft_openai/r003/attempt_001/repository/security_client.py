from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient


def get_security_client(config):
    with DefaultAzureCredential() as credential:
        return KeyClient(config['key_vault_url'], credential)


def get_cryptography_client(key_id, config):
    with DefaultAzureCredential() as credential:
        return CryptographyClient(key_id, credential)
