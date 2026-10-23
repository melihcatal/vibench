import os
import json
from typing import Dict
from security_client import SecretManagerHelper

# Google Cloud Project ID can be set as an environment variable
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")


def fetch_db_secret(secret_id: str) -> Dict[str, str]:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = SecretManagerHelper(project_id=PROJECT_ID)
    secret_payload = client.get_secret_value(secret_id)

    # Assuming the DB secret is stored as a JSON string
    db_config_str = secret_payload.data.decode("utf-8")
    db_config = json.loads(db_config_str)
    return db_config


# Example Usage (replace with actual secret_id and set GOOGLE_CLOUD_PROJECT_ID env var)
if __name__ == "__main__":
    try:
        db_secret = fetch_db_secret("my-database-secret")
        print(f"Fetched DB Secret Host: {db_secret.get('host')}")
        print(f"Fetched DB Secret User: {db_secret.get('username')}")
    except Exception as e:
        print(f"Error fetching DB secret: {e}")
