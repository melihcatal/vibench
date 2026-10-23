from google.cloud import secretmanager


def summarize_rotation_status(payload, config=None):
    config = config or {}
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{config['project_id']}/secrets/{payload['secret_id']}"
    secret = client.get_secret(request={"name": name})
    versions = client.list_secret_versions(request={"parent": secret.name})
    rotation_status = {"current_version": secret.version_id, "total_versions": len(versions.versions)}
    return rotation_status