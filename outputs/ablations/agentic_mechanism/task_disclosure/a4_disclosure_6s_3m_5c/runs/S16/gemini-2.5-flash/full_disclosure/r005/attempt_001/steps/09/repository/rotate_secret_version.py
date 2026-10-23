from google.cloud import secretmanager_v1 as secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the payload for the given secret version if it exists. The version
    can be a version number or an alias (e.g. "latest").
    """
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(name=name)

    return response.payload.data.decode("UTF-8")
