import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


# Provide local configuration and client helper utilities for Secret Management
def get_secret_client():
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    return client
