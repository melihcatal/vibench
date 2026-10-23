import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=credential)

def get_rotation_summary(secret_name):
    properties = client.get_secret_properties(secret_name)
    return { 'enabled': properties.enabled,'versions': [v.name for v in properties.recoverable_secret_versions] }