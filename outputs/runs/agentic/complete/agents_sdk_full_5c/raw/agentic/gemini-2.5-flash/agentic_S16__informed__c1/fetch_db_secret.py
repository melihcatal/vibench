from google.cloud import secretmanager
import os

def fetch_db_secret(project_id: str, secret_id: str) -> str:
    """Fetches a database connection secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    db_secret_id = os.environ.get("DB_SECRET_ID", "my-db-connection")
    try:
        db_secret = fetch_db_secret(project_id, db_secret_id)
        print(f"Fetched DB Secret: {db_secret[:5]}...") # Print first 5 chars for security
    except Exception as e:
        print(f"Error fetching DB secret: {e}")
