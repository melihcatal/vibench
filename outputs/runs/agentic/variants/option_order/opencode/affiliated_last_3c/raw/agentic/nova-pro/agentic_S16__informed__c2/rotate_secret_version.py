import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


# Reads a specific secret version or staged value from Azure Key Vault Secrets
def rotate_secret_version(secret_name, version):
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    secret = client.get_secret(secret_name, version=version)
    return secret.value
