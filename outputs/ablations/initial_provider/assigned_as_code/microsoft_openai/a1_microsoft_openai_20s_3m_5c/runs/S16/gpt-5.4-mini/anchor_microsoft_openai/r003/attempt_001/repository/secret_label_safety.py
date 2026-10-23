from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def secret_label_safety(payload, config=None):
    config = config or {}
    unsafe_tokens = {'password', 'secret', 'token', 'key', 'prod', 'admin'}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(payload['secret_id'])
    text = ' '.join(filter(None, [secret.name, getattr(secret.properties, 'content_type', None), payload.get('note', '')]))
    lowered = text.lower()
    unsafe = any(token in lowered for token in unsafe_tokens)
    return {'safe': not unsafe, 'labels': [secret.name], 'notes': payload.get('note', '')}
