from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient


def key_usage_summary(config):
    with DefaultAzureCredential() as credential:
        key_client = KeyClient(config['key_vault_url'], credential)
        keys = key_client.list_properties_of_keys()
        summary = {}
        for key in keys:
            summary[key.name] = key.attributes.created_on
        return summary
