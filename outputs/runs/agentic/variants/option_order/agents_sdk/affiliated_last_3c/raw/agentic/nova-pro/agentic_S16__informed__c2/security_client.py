from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_secret_client(key_vault_name):
    key_vault_url = f'https://{key_vault_name}.vault.azure.net/'
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=key_vault_url, credential=credential)