import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches a database connection secret from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret to fetch.
        version_id: The version of the secret to fetch (e.g., "latest" or a specific version number).

    Returns:
        The secret payload as a string.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with your actual project_id and secret_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    db_secret_id = "my-database-connection-secret" # Replace with your secret ID

    if project_id:
        try:
            secret_value = fetch_db_secret(project_id, db_secret_id)
            print(f"Successfully fetched secret: {secret_value}")
        except Exception as e:
            print(f"Error fetching secret: {e}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
