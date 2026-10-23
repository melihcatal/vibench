from google.cloud import secretmanager


def secret_audit_embedding(project_id: str, secret_id: str) -> list:
    client = secretmanager.SecretManagerServiceClient()
    secret = client.get_secret(request={"name": f"projects/{project_id}/secrets/{secret_id}"})
    text = " ".join(filter(None, [secret.name, getattr(secret, "etag", ""), " ".join(f"{k}={v}" for k, v in dict(secret.labels).items())]))
    return [float((ord(ch) % 32) / 31.0) for ch in text[:64]]
