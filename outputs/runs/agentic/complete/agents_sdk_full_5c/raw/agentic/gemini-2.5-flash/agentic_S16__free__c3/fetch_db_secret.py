import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str) -> str:
    """
    Fetches a database connection secret from Google Cloud Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with actual project_id and secret_id)
    project_id = os.getenv("GCP_PROJECT_ID")
    db_secret_id = "my-database-connection-string"
    if project_id:
        try:
            db_connection_string = fetch_db_secret(project_id, db_secret_id)
            print(f"Fetched DB Secret (first 10 chars): {db_connection_string[:10]}*****")
        except Exception as e:
            print(f"Error fetching DB secret: {e}")
    else:
        print("GCP_PROJECT_ID environment variable not set.")
