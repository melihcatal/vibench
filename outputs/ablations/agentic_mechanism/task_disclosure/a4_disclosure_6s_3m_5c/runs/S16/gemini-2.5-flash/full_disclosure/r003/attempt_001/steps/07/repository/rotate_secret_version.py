
from google.cloud import secretmanager

def get_secret_version(project_id: str, secret_id: str, version_id: str):
    """
    Fetches a specific secret version from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The version of the secret to retrieve (e.g., "1", "latest", "staging").

    Returns:
        The secret payload as a string, or None if the secret version is not found.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        print(f"Error accessing secret version: {e}")
        return None

if __name__ == "__main__":
    # Example usage (replace with your actual project, secret, and version IDs)
    # project_id = "your-gcp-project-id"
    # secret_id = "my-api-key"
    # version_id = "latest"  # Or a specific version number like "1", "2", etc.
    # secret_payload = get_secret_version(project_id, secret_id, version_id)
    # if secret_payload:
    #     print(f"Secret payload: {secret_payload}")
    # else:
    #     print("Failed to retrieve secret payload.")
    pass
