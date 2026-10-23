import os
from typing import Optional

from google.cloud import secretmanager


def fetch_db_secret(secret_name: Optional[str] = None, project_id: Optional[str] = None) -> str:
    client = secretmanager.SecretManagerServiceClient()
    project = project_id or os.environ["GOOGLE_CLOUD_PROJECT"]
    name = secret_name or os.environ["DB_SECRET_NAME"]
    resource = f"projects/{project}/secrets/{name}/versions/latest"
    response = client.access_secret_version(request={"name": resource})
    return response.payload.data.decode("utf-8")
