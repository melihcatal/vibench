from google.cloud import secretmanager


def embed_secret_audit_notes(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    notes = secret.labels.get('audit_notes', '')
    # Placeholder for embedding logic
    embedded_notes = {"embedded_notes": notes}
    return embedded_notes