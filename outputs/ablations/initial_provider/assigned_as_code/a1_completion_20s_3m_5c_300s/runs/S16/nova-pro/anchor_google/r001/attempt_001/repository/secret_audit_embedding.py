from google.cloud import secretmanager


def embed_secret_audit_notes(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": name})
    notes = secret.labels.get('audit_notes', '')
    # Placeholder for actual embedding logic
    embedded_notes = notes.replace(' ', '_')
    return embedded_notes