from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config, get_secret_name


def rotate_secret_version(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(get_secret_name(payload, 'secret_id'), version=payload.get('version'))
    return {'secret_value': secret.value, 'version': secret.properties.version}
