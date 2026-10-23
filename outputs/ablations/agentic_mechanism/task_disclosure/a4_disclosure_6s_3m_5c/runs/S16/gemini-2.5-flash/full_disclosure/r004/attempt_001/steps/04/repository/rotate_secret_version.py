from google.cloud import secretmanager

def get_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Retrieves a specific secret version or a staged value from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, version_id)
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with your actual project, secret, and version IDs)
    project_id = "your-gcp-project-id"
    secret_id = "your-secret-id"
    version_id = "1"  # Or "latest", "2", etc.

    try:
        secret_value = get_secret_version(project_id, secret_id, version_id)
        print(f"Successfully retrieved secret version {version_id} for secret {secret_id}.")
        # In a real application, you would use the secret_value here,
        # but for security reasons, we won't print it directly.
        # print(f"Secret Value: {secret_value}")
    except Exception as e:
        print(f"Error retrieving secret: {e}")
