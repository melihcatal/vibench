from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload.
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID, Secret ID, and Version ID
    project_id = "your-gcp-project-id"
    secret_id = "your-secret-id"
    version_id = "latest"  # Or a specific version number like "1", "2", etc.

    try:
        secret_value = access_secret_version(project_id, secret_id, version_id)
        print(f"Secret value: {secret_value}")
    except Exception as e:
        print(f"Error accessing secret: {e}")
