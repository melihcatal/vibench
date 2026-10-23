import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def get_secret_client():
    return SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=DefaultAzureCredential())