import os
from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Reads a specific secret version from Google Secret Manager.
    This function simulates accessing a secret version after a rotation,
    where `version_id` would point to the newly rotated version.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    secret_id = "my-rotate-secret"
    specific_version_id = "2" # Example: access version 2
    try:
        rotated_secret_value = rotate_secret_version(project_id, secret_id, specific_version_id)
        print(f"Successfully read secret version {specific_version_id} (first 5 chars): {rotated_secret_value[:5]}...")
    except Exception as e:
        print(f"Error reading specific secret version: {e}")
