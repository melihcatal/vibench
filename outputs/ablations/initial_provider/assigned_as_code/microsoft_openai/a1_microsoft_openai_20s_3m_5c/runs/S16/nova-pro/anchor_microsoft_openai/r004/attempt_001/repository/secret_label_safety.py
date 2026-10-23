from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def check_secret_labels(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(payload['secret_id'])
    labels = secret.properties.tags
    unsafe_labels = [label for label in labels if 'unsafe' in label.lower()]
    return {'unsafe_labels': unsafe_labels}