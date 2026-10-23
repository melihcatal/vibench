import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=credential)

def fetch_api_key(secret_name):
    return client.get_secret(secret_name).value