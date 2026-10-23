from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def secret_label_safety(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(payload['secret_id'])
    text = ' '.join([secret.name or '', payload.get('note') or '', payload.get('label') or '']).lower()
    unsafe = any(term in text for term in ['password', 'token', 'secret', 'private key'])
    return {'safe': not unsafe}
