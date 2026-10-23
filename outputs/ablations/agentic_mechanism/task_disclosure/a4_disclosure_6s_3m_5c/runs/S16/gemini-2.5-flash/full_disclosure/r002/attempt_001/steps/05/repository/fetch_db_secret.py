from google.cloud import secretmanager_v1beta1 as secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest"):
    """
    Fetches a database connection secret from Google Secret Manager at runtime.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = client.secret_version_path(project_id, secret_id, version_id)
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

if __name__ == "__main__":
    # Example usage (replace with your actual project_id and secret_id)
    # project_id = "your-gcp-project-id"
    # secret_id = "your-db-secret-id"
    # db_secret = fetch_db_secret(project_id, secret_id)
    # print(f"Database Secret: {db_secret}")
    pass
