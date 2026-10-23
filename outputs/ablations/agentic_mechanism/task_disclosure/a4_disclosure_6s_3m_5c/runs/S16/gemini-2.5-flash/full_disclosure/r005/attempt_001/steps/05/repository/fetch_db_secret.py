import os
from google.cloud import secretmanager

def fetch_database_secret(project_id: str, secret_id: str, version_id: str = "latest"):
    """
    Fetches a database connection secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with your actual project ID and secret ID)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    db_secret_id = "your-database-secret-id" # e.g., "my-db-connection-string"

    if project_id and db_secret_id:
        try:
            secret_value = fetch_database_secret(project_id, db_secret_id)
            # In a real application, you would use this secret to connect to your database
            # print(f"Successfully fetched database secret (first 10 chars): {secret_value[:10]}...")
        except Exception as e:
            # print(f"Error fetching secret: {e}")
            pass
    else:
        # print("Please set GOOGLE_CLOUD_PROJECT environment variable and 'your-database-secret-id'.")
        pass
