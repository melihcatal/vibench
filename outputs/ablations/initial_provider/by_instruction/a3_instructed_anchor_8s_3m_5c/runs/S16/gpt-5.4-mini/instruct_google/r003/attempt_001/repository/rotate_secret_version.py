from security_client import build_client, get_project_id


def rotate_secret_version(secret_name: str, version: str = "latest"):
    project_id = get_project_id()
    client = build_client()
    resource = f"projects/{project_id}/secrets/{secret_name}/versions/{version}"
    return client.access_secret_version(name=resource)
