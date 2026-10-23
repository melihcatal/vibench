from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def embed_secret_audit_notes(payload, config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        with SecretClient(vault_url=config['vault_url'], credential=credential) as client:
            secret = client.get_secret(payload['secret_id'])
    notes = secret.properties.tags.get('audit_notes', '')
    # Placeholder for actual embedding logic
    embedded_notes = f'Embedded: {notes}'
    return {'embedded_notes': embedded_notes}