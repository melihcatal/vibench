from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

def key_usage_summary(key_id):
    credential = DefaultAzureCredential()
    client = KeyClient(vault_url='https://<your-key-vault-name>.vault.azure.net/', credential=credential)
    key = client.get_key(key_id)
    return key.properties.attributes.created, key.properties.attributes.updated