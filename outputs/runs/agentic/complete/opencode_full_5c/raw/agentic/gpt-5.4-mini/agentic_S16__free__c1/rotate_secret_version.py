from google.cloud import secretmanager

from security_client import build_secret_version_name, get_secret_manager_client


def rotate_secret_version(secret_id: str, version: str = "latest") -> str:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    name = build_secret_version_name(secret_id, version)
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")
