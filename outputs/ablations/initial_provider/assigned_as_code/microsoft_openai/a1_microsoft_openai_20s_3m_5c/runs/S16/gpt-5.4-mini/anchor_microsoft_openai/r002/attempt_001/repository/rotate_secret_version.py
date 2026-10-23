from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def rotate_secret_version(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            version = payload.get('version')
            if version:
                value = client.get_secret(payload['secret_id'], version=version).value
            else:
                value = client.get_secret(payload['secret_id'], version=payload.get('stage')).value
    return {'secret_value': value}
