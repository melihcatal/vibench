import os
from security_client import get_secret_manager_client


def fetch_database_secret(project_id: str, secret_id: str) -> str:
    """
    Fetches a database connection string from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(request={"name": name})
        db_secret = response.payload.data.decode("UTF-8")
        return db_secret
    except Exception as e:
        print(f"Error fetching database secret: {e}")
        return ""


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    secret_id = "database-credentials"
    if project_id:
        secret_value = fetch_database_secret(project_id, secret_id)
        if secret_value:
            print("Successfully fetched database secret.")
    else:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
