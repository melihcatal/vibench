from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """Access the payload for the given secret version if one exists.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return payload

if __name__ == "__main__":
    # Replace with your actual project ID, secret ID, and version ID
    project_id = "your-gcp-project-id"  
    secret_id = "your-secret-id"
    version_id = "your-version-id"  # e.g., "1", "latest"

    try:
        secret_value = access_secret_version(project_id, secret_id, version_id)
        print(f"Secret payload: {secret_value}")
    except Exception as e:
        print(f"Error accessing secret: {e}")
