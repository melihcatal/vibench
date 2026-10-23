from google.cloud import secretmanager_v1

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches a database connection secret from Google Cloud Secret Manager.
    """
    client = secretmanager_v1.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(name=name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise RuntimeError(f"Error accessing secret {secret_id}: {e}")

if __name__ == '__main__':
    # This is an example of how you might use it.
    # In a real scenario, project_id and secret_id would come from environment variables or configuration.
    # DB_SECRET = fetch_db_secret("your-gcp-project-id", "my-database-secret")
    # print(f"Fetched DB Secret (first 5 chars): {DB_SECRET[:5]}...")
    pass
