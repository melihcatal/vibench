import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()
client = SecretClient(vault_url=os.getenv('AZURE_KEYVAULT_URL'), credential=credential)

def rotation_summary(secret_name):
    properties = client.get_secret_properties(secret_name)
    return { 'enabled': properties.enabled, 'created_on': properties.created_on, 'updated_on': properties.updated_on }