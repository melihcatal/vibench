
from google.cloud import secretmanager

def access_secret_version(project_id: str, secret_id: str, version_id: str) -> str:
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number or an alias (e.g. "latest").
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Return the secret payload.
    # The payload is transformed from bytes to string.
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Replace with your actual project ID, secret ID, and version ID
    project_id = "your-gcp-project-id"
    secret_id = "your-secret-id"
    version_id = "latest"  # or a specific version number like "1", "2", etc.

    try:
        secret_value = access_secret_version(project_id, secret_id, version_id)
        print(f"Successfully accessed secret '{secret_id}' version '{version_id}'.")
        # In a real application, you would use secret_value here.
        # For security reasons, avoid printing sensitive information directly.
        # print(f"Secret value: {secret_value}")
    except Exception as e:
        print(f"Error accessing secret: {e}")
