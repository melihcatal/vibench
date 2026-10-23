from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def get_security_client(config):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=config['vault_url'], credential=credential)
    return client