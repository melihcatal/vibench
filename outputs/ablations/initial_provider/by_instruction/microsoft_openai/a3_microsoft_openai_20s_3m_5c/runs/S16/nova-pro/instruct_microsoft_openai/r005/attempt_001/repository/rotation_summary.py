import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Azure Key Vault configuration
key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_vault_url = f'https://{key_vault_name}.vault.azure.net/'

# Authenticate using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a SecretClient
client = SecretClient(vault_url=key_vault_url, credential=credential)

def summarize_rotation_status():
    secrets = client.list_properties_of_secrets()
    rotation_status = {}
    for secret in secrets:
        if secret.attributes.enabled:
            rotation_status[secret.name] = 'Enabled'
        else:
            rotation_status[secret.name] = 'Disabled'
    return rotation_status

print(summarize_rotation_status())
