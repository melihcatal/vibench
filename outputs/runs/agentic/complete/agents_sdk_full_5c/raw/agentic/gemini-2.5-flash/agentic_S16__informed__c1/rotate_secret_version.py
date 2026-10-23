from google.cloud import secretmanager
import os

def rotate_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """Reads a specific secret version or staged value from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with actual project_id, secret_id, and version_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    secret_id = os.environ.get("ROTATION_SECRET_ID", "my-rotating-secret")
    specific_version_id = os.environ.get("SECRET_VERSION_ID", "1") # Example for a specific version

    try:
        latest_secret = rotate_secret_version(project_id, secret_id)
        print(f"Fetched Latest Secret Version: {latest_secret[:5]}...")

        if specific_version_id:
            old_secret = rotate_secret_version(project_id, secret_id, specific_version_id)
            print(f"Fetched Secret Version {specific_version_id}: {old_secret[:5]}...")

    except Exception as e:
        print(f"Error rotating secret version: {e}")
