from google.cloud import secretmanager

def rotation_summary(project_id):
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets = []
    for secret in client.list_secrets(request={"parent": parent}):
        versions = client.list_secret_versions(request={"parent": secret.name})
        version_count = len(list(versions))
        secrets.append({"secret_id": secret.secret_id, "version_count": version_count, "create_time": secret.create_time.isoformat()})
    return secrets
