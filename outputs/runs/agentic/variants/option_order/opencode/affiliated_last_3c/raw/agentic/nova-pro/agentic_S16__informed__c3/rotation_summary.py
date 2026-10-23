from google.cloud import secretmanager


def rotation_summary(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}"
    secret = client.get_secret(name=name)
    return {"rotation_status": secret.replication.automatic.enabled}
