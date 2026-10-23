from google.cloud import secretmanager


def rotation_summary(project_id: str, secret_id: str) -> dict:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": name})
    return {"name": secret.name, "rotation": getattr(secret.rotation, "next_rotation_time", None), "labels": dict(secret.labels)}
