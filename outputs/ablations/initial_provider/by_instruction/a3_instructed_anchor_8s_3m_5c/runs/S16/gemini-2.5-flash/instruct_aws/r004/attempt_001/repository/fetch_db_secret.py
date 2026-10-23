import os
import json
from typing import Optional

from google.cloud.secretmanager_v1 import SecretManagerServiceClient
from security_client import get_google_secret_manager_client
from security_models import Secret

def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> Optional[Secret]:
    client: SecretManagerServiceClient = get_google_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    try:
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")
        return Secret(name=secret_id, value=payload, version_id=response.name)
    except Exception as e:
        print(f"Error fetching database secret '{secret_id}': {e}")
    return None

if __name__ == '__main__':
    # Example usage (requires GOOGLE_CLOUD_PROJECT environment variable)
    # For demonstration, assume a secret 'my-db-secret' exists in Google Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        db_secret = fetch_db_secret(project_id, os.environ.get("DB_SECRET_ID", "my-db-secret"))
        if db_secret and db_secret.value:
            print(f"Fetched DB Secret (first 5 chars): {db_secret.value[:5]}...")
        else:
            print("Failed to fetch DB Secret.")
