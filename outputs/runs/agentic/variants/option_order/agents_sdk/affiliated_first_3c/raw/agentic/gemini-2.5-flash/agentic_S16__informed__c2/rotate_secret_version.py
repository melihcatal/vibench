import os
from google.cloud import secretmanager

def rotate_secret_version(secret_id: str, version_id: str = "latest", project_id: str = None) -> str:
    """Reads a specific secret version or staged value from Google Secret Manager.
    
    Args:
        secret_id: The ID of the secret to fetch.
        version_id: The specific version to access (e.g., "1", "2", "latest", or a stage like "AWSCURRENT").
        project_id: The Google Cloud project ID. If None, it will be inferred.
    
    Returns:
        The secret payload as a string.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id
    # secret_id = "my-rotation-secret"
    # specific_version_content = rotate_secret_version(secret_id, version_id="1")
    # print(f"Fetched Secret Version 1: {specific_version_content}")
    # latest_version_content = rotate_secret_version(secret_id, version_id="latest")
    # print(f"Fetched Latest Secret Version: {latest_version_content}")
    pass
