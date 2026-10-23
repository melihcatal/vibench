import os
from google.cloud import secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches a database connection secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    db_secret_id = "my-database-connection-string" # Replace with your secret ID

    if project_id:
        try:
            db_conn_str = fetch_db_secret(project_id, db_secret_id)
            print(f"Successfully fetched DB secret (first 10 chars): {db_conn_str[:10]}...")
        except Exception as e:
            print(f"Error fetching DB secret: {e}")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
