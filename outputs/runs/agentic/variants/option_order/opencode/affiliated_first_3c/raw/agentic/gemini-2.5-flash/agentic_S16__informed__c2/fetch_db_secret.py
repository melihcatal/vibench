from google.cloud import secretmanager
import os


def fetch_db_secret(project_id: str, secret_id: str) -> str:
    """Fetches a database connection secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    db_secret_id = os.environ.get("DB_SECRET_ID", "my-database-secret")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    db_connection_string = fetch_db_secret(project_id, db_secret_id)
    print(
        f"Fetched DB Secret: {db_connection_string[:10]}..."
    )  # Print a portion for security
