
from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the payload for the given secret version if it exists. The version
    can be a version number or an alias (e.g. "latest").
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the secret payload.
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Replace with your actual project ID, secret ID, and version ID
    project_id = "your-gcp-project-id"  # e.g., "my-project-12345"
    secret_id = "my-secret"
    version_id = "latest"  # or a specific version number like "1", "2", etc.

    try:
        secret_value = access_secret_version(project_id, secret_id, version_id)
        print(f"Secret payload: {secret_value}")
    except Exception as e:
        print(f"Error accessing secret: {e}")
