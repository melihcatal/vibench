from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def summarize_rotation_status(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            properties = client.get_secret_properties(payload['secret_id'])
    status = properties.attributes.enabled
    return {'rotation_status': status}