import os
from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Reads a specific secret version from Google Secret Manager.
    Note: Actual rotation typically involves creating a new version and updating its state.
    This function demonstrates accessing a specific version.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "my-rotate-secret" # Replace with your secret ID
    version_to_read = "1" # Replace with a specific version number, e.g., '1', '2'

    if project_id:
        try:
            secret_value = rotate_secret_version(project_id, secret_id, version_to_read)
            print(f"Successfully read secret version '{version_to_read}' (first 5 chars): {secret_value[:5]}...")
        except Exception as e:
            print(f"Error reading secret version: {e}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
