from google.cloud import secretmanager


def secret_label_safety(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    labels = dict(secret.labels)
    notes = payload.get("notes", "")
    unsafe = any(word in notes.lower() for word in ("password", "token", "secret", "private key")) or any(word in " ".join(labels.values()).lower() for word in ("password", "token", "secret", "private key"))
    return {"safe": not unsafe, "labels": labels}
