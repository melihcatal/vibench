from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_secret_version(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            if payload.get('version_id'):
                # Fetch a specific version
                secret_bundle = client.get_secret(payload['secret_id'], version=payload['version_id'])
            else:
                # Fetch the current version
                secret_bundle = client.get_secret(payload['secret_id'])
            
            return {
                'secret_id': secret_bundle.name,
                'version_id': secret_bundle.id.split('/')[-1] if secret_bundle.id else None,
                'value': secret_bundle.value,
                'content_type': secret_bundle.content_type,
                'tags': secret_bundle.tags
            }
