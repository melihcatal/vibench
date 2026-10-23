from google.cloud import secretmanager
import os
from security_models import SecretRequest, SecretResponse

def fetch_db_secret(req: SecretRequest) -> SecretResponse:
    project_id = req.project or os.getenv("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.Client()
    name = f"projects/{project_id}/secrets/{req.name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    value = response.payload.data.decode("UTF-8")
    return SecretResponse(value=value, version=response.name.split("/")[-1])