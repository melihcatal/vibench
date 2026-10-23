import os
from security_client import get_secret_manager_client


def read_secret_by_version(project_id: str, secret_id: str, version: str) -> str:
    """
    Reads a specific version of a secret from Google Cloud Secret Manager.
    'version' can be a version number or a stage like 'latest'.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"

    try:
        response = client.access_secret_version(request={"name": name})
        secret_value = response.payload.data.decode("UTF-8")
        return secret_value
    except Exception as e:
        print(f"Error reading secret version: {e}")
        return ""


if __name__ == "__main__":
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "service-account-key"
    version_id = "2"

    if project:
        secret = read_secret_by_version(project, secret_id, version_id)
        if secret:
            print(f"Successfully read secret version {version_id}.")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
