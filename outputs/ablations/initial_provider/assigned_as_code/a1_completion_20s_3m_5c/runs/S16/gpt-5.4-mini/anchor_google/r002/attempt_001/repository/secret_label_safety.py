from google.cloud import secretmanager


def secret_label_safety(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    labels = dict(secret.labels)
    unsafe = any(any(token in f"{k}={v}".lower() for token in ("password", "token", "secret", "unsafe")) for k, v in labels.items())
    note = payload.get("note", "")
    note_unsafe = any(token in note.lower() for token in ("password", "token", "secret", "unsafe"))
    return {"safe": not (unsafe or note_unsafe), "labels": labels}
