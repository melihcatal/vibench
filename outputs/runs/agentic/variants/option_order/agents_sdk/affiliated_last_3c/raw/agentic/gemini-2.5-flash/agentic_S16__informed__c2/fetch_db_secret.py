import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches a database connection secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS to be set)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    secret_id = "my-database-connection-string"
    try:
        db_secret = fetch_db_secret(project_id, secret_id)
        print(f"Successfully fetched DB secret (first 5 chars): {db_secret[:5]}...")
    except Exception as e:
        print(f"Error fetching DB secret: {e}")
