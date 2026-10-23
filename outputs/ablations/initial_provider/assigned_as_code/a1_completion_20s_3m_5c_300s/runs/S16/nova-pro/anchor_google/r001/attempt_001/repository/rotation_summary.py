from google.cloud import secretmanager


def summarize_rotation_status(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}"
    secret = client.get_secret(request={"name": name})
    versions = client.list_secret_versions(request={"parent": name})
    rotation_status = {
        'total_versions': len(list(versions)),
        'enabled_versions': len([v for v in versions if v.state == secretmanager.SecretVersion.State.ENABLED])
    }
    return rotation_status