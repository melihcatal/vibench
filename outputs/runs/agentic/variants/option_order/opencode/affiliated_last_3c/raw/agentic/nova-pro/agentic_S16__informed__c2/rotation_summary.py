import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


# Summarize secret rotation status
def rotation_summary(secret_name):
    key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
    key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    secret_properties = client.get_secret_properties(secret_name)
    return secret_properties.attributes.recovery_level
