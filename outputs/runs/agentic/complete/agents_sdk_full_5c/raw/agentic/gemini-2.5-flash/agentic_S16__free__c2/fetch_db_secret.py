import os
import google.cloud.secretmanager as secretmanager

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> str:
    """
    Fetches a database connection secret from Google Secret Manager.
    """
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return payload
    except Exception as e:
        raise Exception(f"Failed to retrieve secret {secret_id} version {version_id}: {e}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or use gcloud auth
    # project = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
    # secret = "my-db-secret"
    # db_secret = fetch_db_secret(project, secret)
    # print(f"Fetched DB Secret: {db_secret}")
    pass
