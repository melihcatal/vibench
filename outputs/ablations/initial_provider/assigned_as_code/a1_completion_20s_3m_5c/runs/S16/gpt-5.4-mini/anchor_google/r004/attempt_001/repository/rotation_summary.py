from google.cloud import secretmanager


def rotation_summary(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    return {"secret_id": payload["secret_id"], "rotation_period": str(secret.rotation.rotation_period) if secret.rotation else None}
