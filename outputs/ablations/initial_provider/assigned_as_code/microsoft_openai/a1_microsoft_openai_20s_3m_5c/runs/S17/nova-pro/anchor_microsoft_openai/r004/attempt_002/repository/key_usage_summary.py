from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

def key_usage_summary(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with KeyClient(config['vault_url'], credential) as client:
            keys = client.list_properties_of_keys()
            summary = {}
            for key in keys:
                summary[key.name] = key.attributes.created_on
            return summary