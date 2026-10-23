import os

from google.cloud import secretmanager


def fetch_api_key() -> str:
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
    secret_id = os.environ["GOOGLE_SECRET_MANAGER_SECRET_ID"]
    version = os.getenv("GOOGLE_SECRET_MANAGER_SECRET_VERSION", "latest")
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")
