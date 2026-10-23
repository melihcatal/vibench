from google.cloud import secretmanager
import os

def rotate_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Reads a specific secret version or staged value from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage:
    # project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    # secret_id = "my-rotation-secret"
    # specific_version_secret = rotate_secret_version(project_id, secret_id, "1") # Example for version '1'
    # print(f"Fetched specific version secret: {specific_version_secret}")
    # latest_version_secret = rotate_secret_version(project_id, secret_id) # Example for latest version
    # print(f"Fetched latest version secret: {latest_version_secret}")
    pass
