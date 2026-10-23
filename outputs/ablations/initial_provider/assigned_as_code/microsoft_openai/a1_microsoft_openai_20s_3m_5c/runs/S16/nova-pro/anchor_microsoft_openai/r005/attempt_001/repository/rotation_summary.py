from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from security_client import get_security_client


def summarize_rotation_status(vault_url, secret_id):
    client = get_security_client(vault_url)
    properties = client.get_secret_properties(secret_id)
    versions = client.list_secret_versions(secret_id)
    rotation_status = {
        'secret_id': secret_id,
        'enabled': properties.enabled,
        'versions': [version.name for version in versions]
    }
    return rotation_status
