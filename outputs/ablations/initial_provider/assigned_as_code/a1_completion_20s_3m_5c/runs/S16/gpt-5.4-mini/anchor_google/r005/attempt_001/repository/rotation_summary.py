from google.cloud import secretmanager


def rotation_summary(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    return {"rotation_summary": {"name": secret.name, "labels": dict(secret.labels), "rotation": str(secret.rotation)}}
