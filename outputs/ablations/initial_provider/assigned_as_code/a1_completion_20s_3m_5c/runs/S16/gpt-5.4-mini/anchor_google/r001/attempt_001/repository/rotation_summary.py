from google.cloud import secretmanager


def rotation_summary(payload, config=None):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{payload['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    return {"rotation_period": str(secret.rotation.rotation_period), "next_rotation_time": str(secret.next_rotation_time)}
