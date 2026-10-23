from google.cloud import secretmanager


def secret_audit_embedding(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    notes = payload.get("notes", "")
    text = f"{secret.name} {notes}"
    embedding = [float(ord(ch) % 31) / 31.0 for ch in text[:64]]
    return {"embedding": embedding}
