import os
from security_client import SecurityClient

def fetch_db_secret(project_id: str, secret_id: str) -> str:
    client = SecurityClient()
    db_secret_payload = client.access_secret_version(project_id, secret_id)
    return db_secret_payload.data.decode('utf-8')

if __name__ == '__main__':
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    db_secret_id = "my-database-connection-string"
    # print(f"Fetched DB Secret: {fetch_db_secret(project_id, db_secret_id)}")
