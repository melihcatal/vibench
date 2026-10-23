import os
import json
from security_client import get_secret_manager_client

def fetch_db_secret(secret_name: str) -> dict:
    """
    Fetch a database connection secret from Google Cloud Secret Manager.
    """
    client = get_secret_manager_client()
    response = client.access_secret_version(request={
        "name": f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/secrets/{secret_name}/versions/latest"
    })
    return json.loads(response.payload.data.decode("UTF-8"))