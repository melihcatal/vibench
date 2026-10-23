from google.cloud import secretmanager


def secret_label_safety(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    unsafe = any(token in (secret.labels or {}).get("notes", "").lower() for token in ["password", "token", "secret", "unsafe"])
    return {"safe": not unsafe, "labels": dict(secret.labels or {})}
