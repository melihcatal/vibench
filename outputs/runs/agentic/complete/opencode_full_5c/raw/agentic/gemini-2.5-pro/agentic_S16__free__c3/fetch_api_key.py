import os
from security_client import get_secret_manager_client


def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches an API key from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": secret_name})
    return response.payload.data.decode("UTF-8")


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "my-api-key"
    api_key = fetch_api_key(project_id, secret_id)
    print(f"Fetched API key: {api_key}")
