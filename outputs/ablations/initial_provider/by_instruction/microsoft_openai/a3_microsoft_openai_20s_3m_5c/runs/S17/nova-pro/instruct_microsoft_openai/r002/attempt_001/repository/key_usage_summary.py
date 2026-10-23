import os
from azure.keyvault.keys import KeyClient
from azure.identity import DefaultAzureCredential

key_vault_name = os.getenv('AZURE_KEY_VAULT_NAME')
key_client = KeyClient(vault_url=f'https://{key_vault_name}.vault.azure.net/', credential=DefaultAzureCredential())

def summarize_key_usage():
    keys = key_client.list_properties_of_keys()
    usage_summary = {}
    for key in keys:
        usage_summary[key.name] = key.attributes.created
    return usage_summary
