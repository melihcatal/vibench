import os
from google.cloud import secretmanager

def rotate_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Reads a specific secret version or staged value from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.getenv("GCP_PROJECT_ID")
    secret_id = "my-rotating-secret"
    specific_version = "1" # Or 'latest', '2', etc.
    if project_id:
        try:
            secret_value = rotate_secret_version(project_id, secret_id, specific_version)
            print(f"Fetched Secret (version {specific_version}, first 5 chars): {secret_value[:5]}*****")

            latest_secret_value = rotate_secret_version(project_id, secret_id, "latest")
            print(f"Fetched Latest Secret (first 5 chars): {latest_secret_value[:5]}*****")
        except Exception as e:
            print(f"Error fetching secret version: {e}")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
