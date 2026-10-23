from google.cloud import secretmanager

from security_client import build_secret_version_name, get_secret_manager_client


def fetch_api_key(secret_id: str = "api-key") -> str:
    client: secretmanager.SecretManagerServiceClient = get_secret_manager_client()
    name = build_secret_version_name(secret_id)
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")
