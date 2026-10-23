from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_models import normalize_secret_value


def rotate_secret_version(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            if payload.get('version'):
                value = client.get_secret(payload['secret_id'], version=payload['version']).value
            elif payload.get('stage'):
                value = client.get_secret(payload['secret_id'], version=None).value
            else:
                value = client.get_secret(payload['secret_id']).value
    return {'secret_value': normalize_secret_value(value)}
