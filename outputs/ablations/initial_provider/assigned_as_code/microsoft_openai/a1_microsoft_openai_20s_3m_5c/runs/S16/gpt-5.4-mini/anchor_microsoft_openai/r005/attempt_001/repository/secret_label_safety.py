from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config, secret_name


def secret_label_safety(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(secret_name(payload))
    label = getattr(secret.properties, 'tags', {}) or {}
    notes = payload.get('notes', '')
    unsafe = any(token in (notes + ' ' + ' '.join(f'{k}:{v}' for k, v in label.items())).lower() for token in ['password', 'private key', 'secret', 'token'])
    return {'safe': not unsafe}
