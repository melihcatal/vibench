from google.cloud import secretmanager


def secret_label_safety(project_id: str, secret_id: str) -> bool:
    client = secretmanager.SecretManagerServiceClient()
    secret = client.get_secret(request={"name": f"projects/{project_id}/secrets/{secret_id}"})
    text = " ".join([secret.name or "", " ".join(f"{k}={v}" for k, v in dict(secret.labels).items())])
    lowered = text.lower()
    unsafe = ["password", "token", "secret", "private key", "ssh"]
    return not any(item in lowered for item in unsafe)
