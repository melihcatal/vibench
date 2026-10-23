from security_client import get_secret_manager_client


def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
