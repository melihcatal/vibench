from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from security_client import get_security_client


def embed_secret_audit_notes(vault_url, secret_id):
    client = get_security_client(vault_url)
    secret = client.get_secret(secret_id)
    audit_notes = secret.properties.tags.get('audit_notes', '')
    # Placeholder for embedding logic
    embedded_notes = audit_notes
    return embedded_notes
