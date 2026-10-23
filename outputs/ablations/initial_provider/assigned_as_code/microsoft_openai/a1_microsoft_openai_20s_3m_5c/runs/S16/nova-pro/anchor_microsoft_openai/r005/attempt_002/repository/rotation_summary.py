from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def summarize_secret_rotation(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            properties = client.get_secret_properties(payload['secret_id'])
            versions = [version.name for version in client.list_secret_versions(payload['secret_id']) if version.enabled]
    return {'rotation_status': {'enabled_versions': versions, 'properties': properties}}