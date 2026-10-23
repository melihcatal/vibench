from google.cloud import secretmanager
import os


def rotate_secret_version(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str:
    """Reads a specific secret version or staged value from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    secret_id = os.environ.get("SECRET_TO_ROTATE_ID", "my-rotating-secret")
    version_to_access = os.environ.get("SECRET_VERSION_ID", "latest")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    secret_value = rotate_secret_version(project_id, secret_id, version_to_access)
    print(f"Fetched Secret Version '{version_to_access}': {secret_value[:10]}...")
