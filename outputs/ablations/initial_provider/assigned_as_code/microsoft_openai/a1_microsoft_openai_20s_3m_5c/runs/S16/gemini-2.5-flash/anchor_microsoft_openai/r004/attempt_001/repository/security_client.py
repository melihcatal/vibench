from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret_client(vault_url):
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=vault_url, credential=credential)
