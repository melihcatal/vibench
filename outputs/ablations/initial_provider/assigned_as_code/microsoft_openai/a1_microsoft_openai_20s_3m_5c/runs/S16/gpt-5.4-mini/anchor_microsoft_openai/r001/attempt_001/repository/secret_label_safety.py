from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from security_client import load_config


def secret_label_safety(payload, config=None):
    config = load_config(config)
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            props = client.get_secret_properties(payload['secret_id'])
    text = ' '.join(filter(None, [getattr(props, 'name', ''), str(getattr(props, 'tags', {})), payload.get('notes', '')]))
    unsafe = any(term in text.lower() for term in ('password', 'token', 'private key', 'secret'))
    return {'safe': not unsafe}
