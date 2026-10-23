import os
from security_client import get_secret_manager_client
from security_models import SecretPayload


def read_secret_version(
    project_id: str, secret_id: str, version_id: str
) -> SecretPayload:
    """
    Reads a specific secret version from Google Cloud Secret Manager.
    This can be a version number or an alias like 'latest' or 'previous'.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return SecretPayload(raw=response.payload.data)


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "rotating-api-key"

    # Fetch the latest version
    latest_version_payload = read_secret_version(project_id, secret_id, "latest")
    print(f"Latest secret version: {latest_version_payload.as_string()}")

    # To read a specific version (e.g., for rotation), you would specify the version number.
    # For this example, we assume version '1' exists.
    try:
        specific_version_payload = read_secret_version(project_id, secret_id, "1")
        print(f"Specific secret version '1': {specific_version_payload.as_string()}")
    except Exception as e:
        print(f"Could not fetch version 1: {e}. This is expected if it doesn't exist.")
