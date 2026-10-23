import os
from security_client import SecretManagerClient
from security_models import SecretRequest


def fetch_db_secret(project_id: str, secret_id: str) -> str:
    client = SecretManagerClient()
    request = SecretRequest(project_id=project_id, secret_id=secret_id)
    response = client.access_secret_version(request)
    return response.payload


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    db_secret_id = "my-database-credentials"
    if project_id:
        db_credentials = fetch_db_secret(project_id, db_secret_id)
        print(f"Fetched DB Secret: {db_credentials}")
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
