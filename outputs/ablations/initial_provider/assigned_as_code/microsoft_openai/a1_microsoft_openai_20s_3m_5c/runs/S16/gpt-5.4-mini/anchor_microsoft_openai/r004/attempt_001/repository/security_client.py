from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def build_secret_client(vault_url):
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)


def get_secret_value(vault_url, secret_id, version=None):
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=vault_url, credential=credential) as client:
            if version:
                return client.get_secret(secret_id, version).value
            return client.get_secret(secret_id).value
