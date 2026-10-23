from google.cloud import secretmanager


def secret_label_safety(payload, config=None):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{payload['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    labels = dict(secret.labels)
    unsafe = any(any(ch in value for ch in ["<", ">", "{", "}", "$"]) for value in labels.values())
    note = payload.get("note", "")
    note_unsafe = any(token in note.lower() for token in ["password", "token", "key", "secret"])
    return {"safe": not (unsafe or note_unsafe)}
